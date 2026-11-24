/**
 * PocketGull First-Party Binary SFNT `loca` + `glyf` + `gvar` Contour & Delta Telemetry Engine
 * Clean-room vanilla JavaScript implementation (Apache-2.0). Zero third-party dependencies.
 * Conceptual homage: Inspired by Thomas Phinney's SFNT forensics (var_spector.dart)
 * and Laurence Penney's variable-font tuple inspection concepts.
 */
(function (root) {
  'use strict';

  function unpackPointNumbers(u8, dv, pos) {
    const b0 = u8[pos++];
    if (b0 === 0) return { points: null, nextPos: pos };
    const count = (b0 & 0x80) ? (((b0 & 0x7F) << 8) | u8[pos++]) : b0;
    const points = [];
    let cur = 0;
    while (points.length < count && pos < u8.length) {
      const ctrl = u8[pos++];
      const runLen = (ctrl & 0x7F) + 1;
      const is16 = (ctrl & 0x80) !== 0;
      for (let i = 0; i < runLen && points.length < count; i++) {
        cur += is16 ? dv.getUint16(pos) : u8[pos];
        pos += is16 ? 2 : 1;
        points.push(cur);
      }
    }
    return { points, nextPos: pos };
  }

  function unpackDeltas(u8, dv, pos, count) {
    const out = new Int32Array(count);
    let idx = 0;
    while (idx < count && pos < u8.length) {
      const ctrl = u8[pos++];
      const runLen = (ctrl & 0x3F) + 1;
      if (ctrl & 0x80) {
        idx += Math.min(runLen, count - idx);
      } else if (ctrl & 0x40) {
        for (let i = 0; i < runLen && idx < count; i++) {
          out[idx++] = dv.getInt16(pos);
          pos += 2;
        }
      } else {
        for (let i = 0; i < runLen && idx < count; i++) {
          out[idx++] = dv.getInt8(pos);
          pos += 1;
        }
      }
    }
    return { deltas: out, nextPos: pos };
  }

  function interpolateUntouchedContour(baseCoords, deltas, touchedFlags, startPt, endPt) {
    const touched = [];
    for (let i = startPt; i <= endPt; i++) {
      if (touchedFlags[i]) touched.push(i);
    }
    if (touched.length === 0) return;
    if (touched.length === 1) {
      const d = deltas[touched[0]];
      for (let i = startPt; i <= endPt; i++) deltas[i] = d;
      return;
    }
    const contourLen = endPt - startPt + 1;
    for (let tIdx = 0; tIdx < touched.length; tIdx++) {
      const pA = touched[tIdx];
      const pB = touched[(tIdx + 1) % touched.length];
      const cA = baseCoords[pA];
      const cB = baseCoords[pB];
      const dA = deltas[pA];
      const dB = deltas[pB];
      const minC = Math.min(cA, cB);
      const maxC = Math.max(cA, cB);
      let step = (pA - startPt + 1) % contourLen + startPt;
      while (step !== pB) {
        const c = baseCoords[step];
        if (c <= minC) {
          deltas[step] = cA <= cB ? dA : dB;
        } else if (c >= maxC) {
          deltas[step] = cA >= cB ? dA : dB;
        } else {
          deltas[step] = dA + ((c - cA) / (cB - cA)) * (dB - dA);
        }
        step = (step - startPt + 1) % contourLen + startPt;
      }
    }
  }

  function parseSfntBuffer(bufferLike) {
    const u8 = bufferLike instanceof Uint8Array
      ? bufferLike
      : new Uint8Array(bufferLike);
    const dv = new DataView(u8.buffer, u8.byteOffset, u8.byteLength);
    const numTables = dv.getUint16(4);
    const tables = {};
    for (let i = 0; i < numTables; i++) {
      const off = 12 + i * 16;
      let tag = '';
      for (let k = 0; k < 4; k++) tag += String.fromCharCode(u8[off + k]);
      tables[tag] = { offset: dv.getUint32(off + 8), length: dv.getUint32(off + 12) };
    }

    const headOff = tables.head.offset;
    const unitsPerEm = dv.getUint16(headOff + 18);
    const isLongLoca = dv.getInt16(headOff + 50) === 1;
    const numGlyphs = dv.getUint16(tables.maxp.offset + 4);

    // Parse loca
    const locaOff = tables.loca.offset;
    const loca = new Uint32Array(numGlyphs + 1);
    for (let i = 0; i <= numGlyphs; i++) {
      loca[i] = isLongLoca
        ? dv.getUint32(locaOff + i * 4)
        : dv.getUint16(locaOff + i * 2) * 2;
    }

    // Parse hmtx
    const numLongHmtx = dv.getUint16(tables.hhea.offset + 34);
    const hmtxOff = tables.hmtx.offset;
    const advWidths = new Uint16Array(numGlyphs);
    const lsbs = new Int16Array(numGlyphs);
    let lastAdv = 500;
    for (let i = 0; i < numGlyphs; i++) {
      if (i < numLongHmtx) {
        lastAdv = dv.getUint16(hmtxOff + i * 4);
        lsbs[i] = dv.getInt16(hmtxOff + i * 4 + 2);
      } else {
        lsbs[i] = dv.getInt16(hmtxOff + numLongHmtx * 4 + (i - numLongHmtx) * 2);
      }
      advWidths[i] = lastAdv;
    }

    // Parse cmap (format 12 preferred, format 4 fallback)
    const cmapOff = tables.cmap.offset;
    const numSub = dv.getUint16(cmapOff + 2);
    let fmt12Off = 0;
    let fmt4Off = 0;
    for (let i = 0; i < numSub; i++) {
      const sub = cmapOff + dv.getUint32(cmapOff + 8 + i * 8);
      const fmt = dv.getUint16(sub);
      if (fmt === 12) fmt12Off = sub;
      else if (fmt === 4 && !fmt4Off) fmt4Off = sub;
    }

    function codepointToGid(cp) {
      if (fmt12Off) {
        const ng = dv.getUint32(fmt12Off + 12);
        let lo = 0;
        let hi = ng - 1;
        while (lo <= hi) {
          const mid = (lo + hi) >>> 1;
          const gp = fmt12Off + 16 + mid * 12;
          const s = dv.getUint32(gp);
          const e = dv.getUint32(gp + 4);
          if (cp < s) hi = mid - 1;
          else if (cp > e) lo = mid + 1;
          else return dv.getUint32(gp + 8) + (cp - s);
        }
      }
      if (fmt4Off && cp <= 0xFFFF) {
        const segX2 = dv.getUint16(fmt4Off + 6);
        const segCnt = segX2 >> 1;
        const endOff = fmt4Off + 14;
        const startOff = endOff + segX2 + 2;
        const deltaOff = startOff + segX2;
        const rangeOff = deltaOff + segX2;
        for (let s = 0; s < segCnt; s++) {
          const end = dv.getUint16(endOff + s * 2);
          if (cp > end) continue;
          const start = dv.getUint16(startOff + s * 2);
          if (cp < start) return 0;
          const delta = dv.getInt16(deltaOff + s * 2);
          const ro = dv.getUint16(rangeOff + s * 2);
          if (ro === 0) return (cp + delta) & 0xFFFF;
          const addr = rangeOff + s * 2 + ro + (cp - start) * 2;
          const raw = dv.getUint16(addr);
          return raw === 0 ? 0 : (raw + delta) & 0xFFFF;
        }
      }
      return 0;
    }

    // Parse fvar
    const axes = [];
    if (tables.fvar) {
      const fv = tables.fvar.offset;
      const ao = fv + dv.getUint16(fv + 4);
      const ac = dv.getUint16(fv + 8);
      const asz = dv.getUint16(fv + 10);
      for (let a = 0; a < ac; a++) {
        const p = ao + a * asz;
        let tag = '';
        for (let k = 0; k < 4; k++) tag += String.fromCharCode(u8[p + k]);
        axes.push({
          tag,
          min: dv.getInt32(p + 4) / 65536,
          def: dv.getInt32(p + 8) / 65536,
          max: dv.getInt32(p + 12) / 65536,
        });
      }
    }

    // Parse gvar header & shared tuples
    let gvar = null;
    if (tables.gvar) {
      const gv = tables.gvar.offset;
      const axisCount = dv.getUint16(gv + 4);
      const sharedTupleCount = dv.getUint16(gv + 6);
      const sharedTuplesOff = gv + dv.getUint32(gv + 8);
      const glyphCount = dv.getUint16(gv + 12);
      const flags = dv.getUint16(gv + 14);
      const dataArrayOff = gv + dv.getUint32(gv + 16);
      const sharedTuples = [];
      for (let s = 0; s < sharedTupleCount; s++) {
        const coords = new Float64Array(axisCount);
        for (let a = 0; a < axisCount; a++) {
          coords[a] = dv.getInt16(sharedTuplesOff + (s * axisCount + a) * 2) / 16384;
        }
        sharedTuples.push(coords);
      }
      gvar = { gv, axisCount, glyphCount, is32BitOff: (flags & 1) !== 0, dataArrayOff, sharedTuples };
    }

    function normalizeAxes(axisValues) {
      const norm = new Float64Array(axes.length);
      for (let a = 0; a < axes.length; a++) {
        const ax = axes[a];
        const raw = axisValues && axisValues[ax.tag] !== undefined ? Number(axisValues[ax.tag]) : ax.def;
        const clamped = Math.min(ax.max, Math.max(ax.min, raw));
        if (clamped === ax.def) norm[a] = 0;
        else if (clamped < ax.def) norm[a] = ax.def > ax.min ? (clamped - ax.def) / (ax.def - ax.min) : 0;
        else norm[a] = ax.max > ax.def ? (clamped - ax.def) / (ax.max - ax.def) : 0;
      }
      return norm;
    }

    function inspectGlyph(charOrGid, axisValues) {
      const gid = typeof charOrGid === 'number'
        ? charOrGid
        : codepointToGid(charOrGid.codePointAt(0));
      const lStart = loca[gid] || 0;
      const lEnd = loca[gid + 1] || lStart;
      const byteLen = lEnd - lStart;
      const baseAw = advWidths[gid] || 500;
      const lsb = lsbs[gid] || 0;

      if (byteLen === 0 || !tables.glyf) {
        return {
          gid, empty: true, locaOffset: lStart, locaEnd: lEnd, glyphByteLength: 0,
          wordAligned: (lStart % 2 === 0) && (lEnd % 2 === 0), bit7Clean: true,
          baseAw, variedAw: baseAw, lsb, rsb: baseAw - lsb, bbox: [0, 0, 0, 0],
          endPts: [], points: [], activeTupleCount: 0, maxDeltaMag: 0,
        };
      }

      const go = tables.glyf.offset + lStart;
      const numContours = dv.getInt16(go);
      const xMin = dv.getInt16(go + 2);
      const yMin = dv.getInt16(go + 4);
      const xMax = dv.getInt16(go + 6);
      const yMax = dv.getInt16(go + 8);

      if (numContours <= 0) {
        return {
          gid, composite: true, locaOffset: lStart, locaEnd: lEnd, glyphByteLength: byteLen,
          wordAligned: (lStart % 2 === 0) && (lEnd % 2 === 0), bit7Clean: true,
          baseAw, variedAw: baseAw, lsb, rsb: baseAw - xMax, bbox: [xMin, yMin, xMax, yMax],
          endPts: [], points: [], activeTupleCount: 0, maxDeltaMag: 0,
        };
      }

      const endPts = [];
      for (let c = 0; c < numContours; c++) {
        endPts.push(dv.getUint16(go + 10 + c * 2));
      }
      const numPoints = endPts[endPts.length - 1] + 1;
      const instLen = dv.getUint16(go + 10 + numContours * 2);
      let p = go + 12 + numContours * 2 + instLen;

      const flags = new Uint8Array(numPoints);
      let bit7Clean = true;
      for (let i = 0; i < numPoints; i++) {
        const f = u8[p++];
        if (f & 0x80) bit7Clean = false;
        flags[i] = f;
        if (f & 0x08) {
          const rep = u8[p++];
          for (let r = 0; r < rep && i + 1 < numPoints; r++) flags[++i] = f;
        }
      }

      const baseX = new Float64Array(numPoints + 4);
      const baseY = new Float64Array(numPoints + 4);
      let curX = 0;
      for (let i = 0; i < numPoints; i++) {
        const f = flags[i];
        if (f & 0x02) {
          const d = u8[p++];
          curX += (f & 0x10) ? d : -d;
        } else if (!(f & 0x10)) {
          curX += dv.getInt16(p);
          p += 2;
        }
        baseX[i] = curX;
      }
      let curY = 0;
      for (let i = 0; i < numPoints; i++) {
        const f = flags[i];
        if (f & 0x04) {
          const d = u8[p++];
          curY += (f & 0x20) ? d : -d;
        } else if (!(f & 0x20)) {
          curY += dv.getInt16(p);
          p += 2;
        }
        baseY[i] = curY;
      }
      // 4 TrueType phantom points
      baseX[numPoints + 1] = baseAw;

      const totalDx = new Float64Array(numPoints + 4);
      const totalDy = new Float64Array(numPoints + 4);
      let activeTupleCount = 0;

      if (gvar && gid < gvar.glyphCount && axes.length > 0) {
        const norm = normalizeAxes(axisValues);
        const offBase = gvar.gv + 20;
        const g1 = gvar.is32BitOff ? dv.getUint32(offBase + gid * 4) : dv.getUint16(offBase + gid * 2) * 2;
        const g2 = gvar.is32BitOff ? dv.getUint32(offBase + (gid + 1) * 4) : dv.getUint16(offBase + (gid + 1) * 2) * 2;

        if (g2 > g1) {
          const gvStart = gvar.dataArrayOff + g1;
          const tcRaw = dv.getUint16(gvStart);
          const tupleCount = tcRaw & 0x0FFF;
          const hasSharedPts = (tcRaw & 0x8000) !== 0;
          let dataCursor = gvStart + dv.getUint16(gvStart + 2);
          let sharedPts = null;
          if (hasSharedPts) {
            const sp = unpackPointNumbers(u8, dv, dataCursor);
            sharedPts = sp.points;
            dataCursor = sp.nextPos;
          }

          let hdrCursor = gvStart + 4;
          const ac = gvar.axisCount;
          for (let t = 0; t < tupleCount; t++) {
            const varDataSize = dv.getUint16(hdrCursor);
            const tupleIndex = dv.getUint16(hdrCursor + 2);
            hdrCursor += 4;

            let peak;
            if (tupleIndex & 0x8000) {
              peak = new Float64Array(ac);
              for (let a = 0; a < ac; a++) {
                peak[a] = dv.getInt16(hdrCursor) / 16384;
                hdrCursor += 2;
              }
            } else {
              peak = gvar.sharedTuples[tupleIndex & 0x0FFF];
            }

            let interStart = null;
            let interEnd = null;
            if (tupleIndex & 0x4000) {
              interStart = new Float64Array(ac);
              interEnd = new Float64Array(ac);
              for (let a = 0; a < ac; a++) {
                interStart[a] = dv.getInt16(hdrCursor) / 16384;
                hdrCursor += 2;
              }
              for (let a = 0; a < ac; a++) {
                interEnd[a] = dv.getInt16(hdrCursor) / 16384;
                hdrCursor += 2;
              }
            }

            const tupleDataEnd = dataCursor + varDataSize;
            let scalar = 1.0;
            for (let a = 0; a < ac; a++) {
              const pk = peak ? peak[a] : 0;
              if (pk === 0) continue;
              const c = norm[a];
              if (c === 0) { scalar = 0; break; }
              const sVal = interStart ? interStart[a] : Math.min(0, pk);
              const eVal = interEnd ? interEnd[a] : Math.max(0, pk);
              if (c < sVal || c > eVal) { scalar = 0; break; }
              if (c < pk) scalar *= (pk > sVal) ? (c - sVal) / (pk - sVal) : 1;
              else if (c > pk) scalar *= (eVal > pk) ? (eVal - c) / (eVal - pk) : 1;
            }

            if (scalar > 1e-6) {
              activeTupleCount++;
              let pos = dataCursor;
              let pts = sharedPts;
              if (tupleIndex & 0x2000) {
                const pp = unpackPointNumbers(u8, dv, pos);
                pts = pp.points;
                pos = pp.nextPos;
              }
              const totalCnt = numPoints + 4;
              const dCnt = pts === null ? totalCnt : pts.length;
              const ux = unpackDeltas(u8, dv, pos, dCnt);
              const uy = unpackDeltas(u8, dv, ux.nextPos, dCnt);

              if (pts === null) {
                for (let i = 0; i < totalCnt; i++) {
                  totalDx[i] += ux.deltas[i] * scalar;
                  totalDy[i] += uy.deltas[i] * scalar;
                }
              } else {
                const tDx = new Float64Array(totalCnt);
                const tDy = new Float64Array(totalCnt);
                const touched = new Uint8Array(totalCnt);
                for (let k = 0; k < pts.length; k++) {
                  const ptIdx = pts[k];
                  if (ptIdx < totalCnt) {
                    touched[ptIdx] = 1;
                    tDx[ptIdx] = ux.deltas[k];
                    tDy[ptIdx] = uy.deltas[k];
                  }
                }
                let cStart = 0;
                for (let c = 0; c < endPts.length; c++) {
                  const cEnd = endPts[c];
                  interpolateUntouchedContour(baseX, tDx, touched, cStart, cEnd);
                  interpolateUntouchedContour(baseY, tDy, touched, cStart, cEnd);
                  cStart = cEnd + 1;
                }
                for (let i = 0; i < totalCnt; i++) {
                  totalDx[i] += tDx[i] * scalar;
                  totalDy[i] += tDy[i] * scalar;
                }
              }
            }
            dataCursor = tupleDataEnd;
          }
        }
      }

      const points = [];
      let vxMin = Infinity, vyMin = Infinity, vxMax = -Infinity, vyMax = -Infinity;
      let maxDeltaMag = 0;
      for (let i = 0; i < numPoints; i++) {
        const dx = totalDx[i];
        const dy = totalDy[i];
        const x = baseX[i] + dx;
        const y = baseY[i] + dy;
        const mag = Math.hypot(dx, dy);
        if (mag > maxDeltaMag) maxDeltaMag = mag;
        if (x < vxMin) vxMin = x;
        if (y < vyMin) vyMin = y;
        if (x > vxMax) vxMax = x;
        if (y > vyMax) vyMax = y;
        points.push({
          index: i,
          baseX: baseX[i],
          baseY: baseY[i],
          x: Math.round(x * 10) / 10,
          y: Math.round(y * 10) / 10,
          dx: Math.round(dx * 10) / 10,
          dy: Math.round(dy * 10) / 10,
          onCurve: (flags[i] & 0x01) !== 0,
        });
      }

      const variedAw = Math.round(baseAw + totalDx[numPoints + 1] - totalDx[numPoints]);
      const finalBbox = points.length > 0
        ? [Math.round(vxMin), Math.round(vyMin), Math.round(vxMax), Math.round(vyMax)]
        : [xMin, yMin, xMax, yMax];

      return {
        gid,
        locaOffset: lStart,
        locaEnd: lEnd,
        glyphByteLength: byteLen,
        wordAligned: (lStart % 2 === 0) && (lEnd % 2 === 0),
        bit7Clean,
        baseAw,
        variedAw,
        lsb: finalBbox[0],
        rsb: variedAw - finalBbox[2],
        bbox: finalBbox,
        endPts,
        points,
        activeTupleCount,
        maxDeltaMag: Math.round(maxDeltaMag * 10) / 10,
      };
    }

    return { unitsPerEm, numGlyphs, axes, codepointToGid, inspectGlyph };
  }

  function traceTrueTypeQuadraticContours(ctx, points, endPts, useBase, ox, oy, scale) {
    let start = 0;
    for (let c = 0; c < endPts.length; c++) {
      const end = endPts[c];
      const len = end - start + 1;
      if (len <= 0) { start = end + 1; continue; }

      const getPt = (idx) => {
        const pt = points[start + ((idx % len + len) % len)];
        return {
          x: ox + (useBase ? pt.baseX : pt.x) * scale,
          y: oy - (useBase ? pt.baseY : pt.y) * scale,
          onCurve: pt.onCurve,
        };
      };

      const p0 = getPt(0);
      const pLast = getPt(len - 1);
      let firstX, firstY, startIdx;
      if (p0.onCurve) {
        firstX = p0.x; firstY = p0.y; startIdx = 1;
      } else if (pLast.onCurve) {
        firstX = pLast.x; firstY = pLast.y; startIdx = 0;
      } else {
        firstX = (pLast.x + p0.x) / 2;
        firstY = (pLast.y + p0.y) / 2;
        startIdx = 0;
      }

      ctx.moveTo(firstX, firstY);
      let i = startIdx;
      while (i < len) {
        const cur = getPt(i);
        if (cur.onCurve) {
          ctx.lineTo(cur.x, cur.y);
          i++;
        } else {
          const next = getPt(i + 1);
          if (next.onCurve) {
            ctx.quadraticCurveTo(cur.x, cur.y, next.x, next.y);
            i += 2;
          } else {
            ctx.quadraticCurveTo(cur.x, cur.y, (cur.x + next.x) / 2, (cur.y + next.y) / 2);
            i += 1;
          }
        }
      }
      if (!p0.onCurve && pLast.onCurve) {
        // Closed via last iteration
      } else if (p0.onCurve) {
        ctx.lineTo(firstX, firstY);
      }
      ctx.closePath();
      start = end + 1;
    }
  }

  function renderGlyphDeltaCanvas(canvas, glyphInfo, theme) {
    if (!canvas || !glyphInfo) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;
    const isWashi = theme === 'washi';
    const isPbm = theme === 'pbm';

    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = isWashi ? '#FAF6EE' : (isPbm ? '#080000' : '#030712');
    ctx.fillRect(0, 0, w, h);

    const scale = Math.min(w / 1450, h / 1180);
    const ox = Math.round((w - glyphInfo.variedAw * scale) / 2);
    const oy = Math.round(h * 0.76);

    // Subtle UPM grid
    ctx.strokeStyle = isWashi ? 'rgba(31, 27, 22, 0.06)' : (isPbm ? 'rgba(239, 68, 68, 0.08)' : 'rgba(255, 255, 255, 0.04)');
    ctx.lineWidth = 1;
    const stepPx = 100 * scale;
    for (let x = ox % stepPx; x < w; x += stepPx) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
    }
    for (let y = oy % stepPx; y < h; y += stepPx) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
    }

    function drawGuide(yUpm, label, color) {
      const cy = oy - yUpm * scale;
      ctx.strokeStyle = color;
      ctx.setLineDash([4, 4]);
      ctx.beginPath(); ctx.moveTo(16, cy); ctx.lineTo(w - 16, cy); ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = color;
      ctx.font = "10px 'PocketGull Mono', monospace";
      ctx.fillText(`${label} (${yUpm})`, 20, cy - 4);
    }

    drawGuide(780, 'sTypoAscender', isWashi ? 'rgba(2, 132, 199, 0.7)' : (isPbm ? 'rgba(239, 68, 68, 0.5)' : 'rgba(56, 189, 248, 0.4)'));
    drawGuide(540, 'x-Height', isWashi ? 'rgba(124, 58, 237, 0.7)' : (isPbm ? 'rgba(220, 38, 38, 0.5)' : 'rgba(167, 139, 250, 0.4)'));
    drawGuide(0, 'Baseline', isWashi ? 'rgba(15, 118, 110, 0.9)' : (isPbm ? 'rgba(239, 68, 68, 0.9)' : 'rgba(45, 212, 191, 0.8)'));
    drawGuide(-180, 'sTypoDescender', isWashi ? 'rgba(185, 28, 28, 0.65)' : (isPbm ? 'rgba(153, 27, 27, 0.5)' : 'rgba(248, 113, 113, 0.35)'));

    // Side-bearing / Advance-Width rails
    const awX = ox + glyphInfo.variedAw * scale;
    const railColor = isWashi ? 'rgba(194, 65, 12, 0.65)' : (isPbm ? 'rgba(248, 113, 113, 0.55)' : 'rgba(251, 146, 60, 0.55)');
    ctx.strokeStyle = railColor;
    ctx.setLineDash([3, 3]);
    ctx.beginPath(); ctx.moveTo(ox, 16); ctx.lineTo(ox, h - 16); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(awX, 16); ctx.lineTo(awX, h - 16); ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = railColor;
    ctx.fillText(`x=0`, ox + 4, 28);
    ctx.fillText(`aw=${glyphInfo.variedAw}`, awX + 4, 28);

    if (glyphInfo.points.length === 0) return { ox, oy, scale };

    // 1. Ghost Default Master Contour (when gvar deltas are active)
    if (glyphInfo.maxDeltaMag >= 0.5) {
      ctx.beginPath();
      traceTrueTypeQuadraticContours(ctx, glyphInfo.points, glyphInfo.endPts, true, ox, oy, scale);
      ctx.strokeStyle = isWashi ? 'rgba(100, 116, 139, 0.45)' : (isPbm ? 'rgba(239, 68, 68, 0.3)' : 'rgba(148, 163, 184, 0.35)');
      ctx.setLineDash([3, 3]);
      ctx.lineWidth = 1.25;
      ctx.stroke();
      ctx.setLineDash([]);
    }

    // 2. Varied Quadratic TrueType Contour (Non-Zero Winding)
    ctx.beginPath();
    traceTrueTypeQuadraticContours(ctx, glyphInfo.points, glyphInfo.endPts, false, ox, oy, scale);
    ctx.fillStyle = isWashi ? 'rgba(15, 118, 110, 0.14)' : (isPbm ? 'rgba(239, 68, 68, 0.16)' : 'rgba(45, 212, 191, 0.15)');
    ctx.fill('nonzero');
    ctx.strokeStyle = isWashi ? '#0f766e' : (isPbm ? '#ef4444' : '#2dd4bf');
    ctx.lineWidth = 2;
    ctx.stroke();

    // 3. Live gvar Displacement Vectors (base -> varied)
    const vecColor = isWashi ? '#be123c' : (isPbm ? '#fca5a5' : '#f43f5e');
    for (let i = 0; i < glyphInfo.points.length; i++) {
      const pt = glyphInfo.points[i];
      const mag = Math.hypot(pt.dx, pt.dy);
      if (mag < 1.0) continue;
      const x0 = ox + pt.baseX * scale;
      const y0 = oy - pt.baseY * scale;
      const x1 = ox + pt.x * scale;
      const y1 = oy - pt.y * scale;
      ctx.strokeStyle = vecColor;
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.moveTo(x0, y0);
      ctx.lineTo(x1, y1);
      ctx.stroke();

      const ang = Math.atan2(y1 - y0, x1 - x0);
      const head = 4.5;
      ctx.fillStyle = vecColor;
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x1 - head * Math.cos(ang - 0.45), y1 - head * Math.sin(ang - 0.45));
      ctx.lineTo(x1 - head * Math.cos(ang + 0.45), y1 - head * Math.sin(ang + 0.45));
      ctx.closePath();
      ctx.fill();
    }

    // 4. On-Curve (●) and Off-Curve Quadratic (○) Control Points
    const onColor = isWashi ? '#0f766e' : (isPbm ? '#ef4444' : '#2dd4bf');
    const offColor = isWashi ? '#d97706' : (isPbm ? '#fbbf24' : '#f59e0b');
    const bgRing = isWashi ? '#FAF6EE' : (isPbm ? '#080000' : '#030712');
    for (let i = 0; i < glyphInfo.points.length; i++) {
      const pt = glyphInfo.points[i];
      const px = ox + pt.x * scale;
      const py = oy - pt.y * scale;
      ctx.beginPath();
      ctx.arc(px, py, pt.onCurve ? 3.6 : 3.2, 0, Math.PI * 2);
      if (pt.onCurve) {
        ctx.fillStyle = onColor;
        ctx.fill();
        ctx.strokeStyle = bgRing;
        ctx.lineWidth = 1.2;
        ctx.stroke();
      } else {
        ctx.fillStyle = bgRing;
        ctx.fill();
        ctx.strokeStyle = offColor;
        ctx.lineWidth = 1.6;
        ctx.stroke();
      }
    }

    return { ox, oy, scale };
  }

  let cachedEnginePromise = null;
  function loadDefaultVfEngine(url) {
    if (!cachedEnginePromise) {
      const targetUrl = url || 'fonts/ttf/PocketGull-VF.ttf';
      cachedEnginePromise = fetch(targetUrl)
        .then((res) => {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          return res.arrayBuffer();
        })
        .then((ab) => parseSfntBuffer(ab));
    }
    return cachedEnginePromise;
  }

  const api = {
    parseSfntBuffer,
    renderGlyphDeltaCanvas,
    loadDefaultVfEngine,
  };

  root.PocketGullBinaryInspector = api;
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
  }
})(typeof globalThis !== 'undefined' ? globalThis : window);
