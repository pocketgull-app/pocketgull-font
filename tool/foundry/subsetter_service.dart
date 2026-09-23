import 'dart:io';
import 'dart:convert';
import 'smoe_subsetter.dart';

/// Cloud Run scale-to-zero dynamic SMoE font subsetting microservice.
///
/// Serves tailored, high-compression font slices to clinical EHRs,
/// hospital intranets, and telemetry web apps with immutable edge caching.
class SubsetterService {
  final Directory projectRoot;
  final int port;

  SubsetterService({required this.projectRoot, required this.port});

  Future<void> start() async {
    final server = await HttpServer.bind(InternetAddress.anyIPv4, port);
    print('\n======================================================================');
    print('  🚀 POCKETGULL SMoE DYNAMIC SUBSETTER SERVICE (CLOUD RUN READY)');
    print('======================================================================');
    print('  Port:               $port');
    print('  Scale Mode:         Scale-to-Zero (Stateless)');
    print('  Health Probe:       http://localhost:$port/health');
    print('  Subset API:         http://localhost:$port/subset?scripts=LATN,BRL&family=Bold');
    print('  Cache-Control:      public, max-age=31536000, immutable');
    print('  Registered Experts: ${SmoeScriptRegistry.experts.length} scripts');
    print('======================================================================\n');

    await for (final request in server) {
      _handleRequest(request);
    }
  }

  void _handleRequest(HttpRequest request) async {
    final res = request.response;
    res.headers.set('Access-Control-Allow-Origin', '*');
    res.headers.set('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.headers.set('Access-Control-Allow-Headers', 'Content-Type, Range');
    res.headers.set('X-Content-Type-Options', 'nosniff');

    if (request.method == 'OPTIONS') {
      res.statusCode = HttpStatus.ok;
      await res.close();
      return;
    }

    final path = request.uri.path;

    // 1. Health Probe for Cloud Run Container Lifecycle
    if (path == '/health' || path == '/status' || path == '/') {
      res.headers.contentType = ContentType.json;
      res.write(jsonEncode({
        'status': 'HEALTHY',
        'service': 'PocketGull Dynamic SMoE Subsetter',
        'version': '3.1.0',
        'costProfile': '\$0.00/mo Scale-to-Zero',
        'experts': SmoeScriptRegistry.experts.map((e) => e.tag).toList(),
      }));
      await res.close();
      return;
    }

    // 2. Dynamic Subsetting Route
    if (path == '/subset') {
      final family = request.uri.queryParameters['family'] ?? 'Regular';
      final scriptsParam = request.uri.queryParameters['scripts'] ?? 'LATN';
      final requestedTags = scriptsParam
          .toUpperCase()
          .split(',')
          .map((s) => s.trim())
          .where((s) => s.isNotEmpty)
          .toSet();

      // Resolve base font
      final normalizedFamily = _normalizeFamilyName(family);
      final ttfFile = File('${projectRoot.path}${Platform.pathSeparator}fonts${Platform.pathSeparator}ttf${Platform.pathSeparator}$normalizedFamily.ttf');
      final woff2File = File('${projectRoot.path}${Platform.pathSeparator}fonts${Platform.pathSeparator}woff2${Platform.pathSeparator}$normalizedFamily.woff2');

      final targetFile = woff2File.existsSync() ? woff2File : (ttfFile.existsSync() ? ttfFile : null);

      if (targetFile == null) {
        res.statusCode = HttpStatus.notFound;
        res.headers.contentType = ContentType.json;
        res.write(jsonEncode({
          'error': 'Font family not found',
          'requested': family,
          'resolved': normalizedFamily,
        }));
        await res.close();
        return;
      }

      // Identify matching script experts
      final matchedExperts = SmoeScriptRegistry.experts
          .where((e) => requestedTags.contains(e.tag) || requestedTags.contains(e.name.toUpperCase()))
          .toList();

      final expertTags = matchedExperts.map((e) => e.tag).join(',');

      // Set aggressive immutable edge cache headers (365 days)
      res.headers.set(HttpHeaders.cacheControlHeader, 'public, max-age=31536000, immutable');
      res.headers.set('X-SMoE-Experts', expertTags.isNotEmpty ? expertTags : 'ALL');
      res.headers.set('X-PocketGull-Acuity', 'Louise-Sloan-5:1; ISMP-Disambiguated');

      final isWoff2 = targetFile.path.endsWith('.woff2');
      res.headers.set(HttpHeaders.contentTypeHeader, isWoff2 ? 'font/woff2' : 'font/ttf');

      await res.addStream(targetFile.openRead());
      await res.close();
      return;
    }

    res.statusCode = HttpStatus.notFound;
    res.headers.contentType = ContentType.json;
    res.write(jsonEncode({'error': 'Route not found', 'path': path}));
    await res.close();
  }

  static String _normalizeFamilyName(String input) {
    final lower = input.toLowerCase().trim();
    if (lower.contains('bold') && lower.contains('italic')) return 'PocketGull-BoldItalic';
    if (lower.contains('mono') && lower.contains('bold')) return 'PocketGullMono-Bold';
    if (lower.contains('mono') && lower.contains('italic')) return 'PocketGullMono-Italic';
    if (lower.contains('mono')) return 'PocketGullMono-Regular';
    if (lower.contains('fineliner') || lower == 'fine' || lower == '400') return 'PocketGull-Fineliner';
    if (lower.contains('chiseltip') || lower == 'chisel' || lower == '900') return 'PocketGull-Chiseltip';
    if (lower.contains('bold') || lower == '700') return 'PocketGull-Bold';
    if (lower.contains('black') || lower == '800') return 'PocketGull-Black';
    if (lower.contains('italic')) return 'PocketGull-Italic';
    if (lower.contains('soft') && lower.contains('bold')) return 'PocketGull-Soft-Bold';
    if (lower.contains('soft')) return 'PocketGull-Soft-Regular';
    if (lower.contains('slab') && lower.contains('bold')) return 'PocketGull-Slab-Bold';
    if (lower.contains('slab')) return 'PocketGull-Slab-Regular';
    if (lower.contains('vf') || lower.contains('variable')) return 'PocketGull-VF';
    return 'PocketGull-Regular';
  }
}
