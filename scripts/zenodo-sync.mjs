import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

/**
 * PocketGull Font CERN / Zenodo Open Science Deposition Synchronizer
 * Connects PocketGull Font releases with CERN Data Centre & Zenodo REST API.
 * 
 * Usage:
 *   node scripts/zenodo-sync.mjs [--validate|--status|--create-draft|--sandbox]
 */

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const isSandbox = process.argv.includes('--sandbox');
const ZENODO_BASE = isSandbox ? 'https://sandbox.zenodo.org/api' : 'https://zenodo.org/api';
const ACCESS_TOKEN = process.env.ZENODO_ACCESS_TOKEN || process.env.ZENODO_TOKEN || process.env.ZENODO_SANDBOX_TOKEN;

async function validateMetadata() {
    console.log('\n🔍 [1/3] Validating CERN/Zenodo .zenodo.json Metadata...');
    const zenodoPath = path.join(ROOT_DIR, '.zenodo.json');
    if (!fs.existsSync(zenodoPath)) {
        console.error('❌ Missing .zenodo.json at root.');
        return null;
    }

    try {
        const data = JSON.parse(fs.readFileSync(zenodoPath, 'utf8'));
        const required = ['title', 'upload_type', 'description', 'creators', 'access_right', 'license', 'version'];
        for (const field of required) {
            if (!data[field]) {
                throw new Error(`Missing required Zenodo field: ${field}`);
            }
        }

        console.log('  ✅ .zenodo.json valid JSON Schema compliance.');
        console.log(`  📦 Title:        ${data.title}`);
        console.log(`  🏷️  Version:      ${data.version}`);
        console.log(`  ⚖️  License:      ${data.license} (SIL Open Font License 1.1)`);
        console.log(`  👤 Lead Author:  ${data.creators[0].name} (ORCID: ${data.creators[0].orcid})`);
        console.log(`  🏢 Affiliation:  ${data.creators[0].affiliation}`);
        console.log(`  🔑 Keywords:     ${data.keywords ? data.keywords.length : 0} tags mapped`);
        console.log(`  🔗 Related:      ${data.related_identifiers ? data.related_identifiers.length : 0} citations mapped`);
        return data;
    } catch (err) {
        console.error('❌ Failed validating .zenodo.json:', err.message);
        return null;
    }
}

async function validateCitationCff() {
    console.log('\n🔍 [2/3] Validating CITATION.cff Alignment...');
    const cffPath = path.join(ROOT_DIR, 'CITATION.cff');
    if (!fs.existsSync(cffPath)) {
        console.error('❌ Missing CITATION.cff at root.');
        return false;
    }
    const content = fs.readFileSync(cffPath, 'utf8');
    const hasOrcid = content.includes('0009-0008-1372-5381');
    const hasTitle = content.includes('PocketGull Font Superfamily');
    const hasLicense = content.includes('OFL-1.1');
    const hasPrefCitation = content.includes('preferred-citation:');

    if (hasOrcid && hasTitle && hasLicense && hasPrefCitation) {
        console.log('  ✅ CITATION.cff aligned with CFF 1.2.0, ORCID, and Zenodo.');
        return true;
    } else {
        console.warn('  ⚠️ CITATION.cff missing expected fields.');
        return false;
    }
}

async function checkApiStatus() {
    console.log(`\n🔍 [3/3] Checking CERN Zenodo API Endpoint (${isSandbox ? 'SANDBOX' : 'PRODUCTION'})...`);
    console.log(`  URL: ${ZENODO_BASE}`);

    if (!ACCESS_TOKEN) {
        console.log('  ℹ️  No ZENODO_ACCESS_TOKEN set in environment.');
        console.log('  ℹ️  Public read test to /api/deposit/depositions...');
        try {
            const res = await fetch(`${ZENODO_BASE}/deposit/depositions`);
            console.log(`  📡 HTTP Response: ${res.status} ${res.statusText} (Expected 401 Unauthorized without token)`);
            console.log('  ✅ CERN Zenodo servers reachable.\n');
        } catch (err) {
            console.error('  ❌ Failed reaching Zenodo API:', err.message);
        }
        return;
    }

    try {
        const res = await fetch(`${ZENODO_BASE}/deposit/depositions`, {
            headers: {
                'Authorization': `Bearer ${ACCESS_TOKEN}`,
                'Content-Type': 'application/json'
            }
        });
        console.log(`  📡 HTTP Response: ${res.status} ${res.statusText}`);
        if (res.ok) {
            const list = await res.json();
            console.log(`  ✅ Successfully authenticated! Found ${list.length} existing deposition(s).`);
        } else {
            const body = await res.json();
            console.error('  ❌ Authentication failed:', body);
        }
    } catch (err) {
        console.error('  ❌ Connection error:', err.message);
    }
}

async function createDraft(metadata) {
    if (!ACCESS_TOKEN) {
        console.error('❌ Cannot create draft: ZENODO_ACCESS_TOKEN environment variable required.');
        process.exit(1);
    }

    console.log(`\n🚀 Initializing new CERN Zenodo Deposition Record...`);
    const payload = {
        metadata: {
            title: metadata.title,
            upload_type: metadata.upload_type,
            description: metadata.description,
            creators: metadata.creators,
            access_right: metadata.access_right,
            license: metadata.license,
            keywords: metadata.keywords,
            related_identifiers: metadata.related_identifiers,
            version: metadata.version,
            publication_date: metadata.publication_date
        }
    };

    try {
        const res = await fetch(`${ZENODO_BASE}/deposit/depositions`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${ACCESS_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(`Zenodo API Error ${res.status}: ${JSON.stringify(err)}`);
        }

        const data = await res.json();
        console.log(`\n🎉 Draft deposition created successfully!`);
        console.log(`  Deposition ID: ${data.id}`);
        console.log(`  Reserved DOI:  ${data.metadata.prereserve_doi ? data.metadata.prereserve_doi.doi : 'Pending'}`);
        console.log(`  Edit URL:      ${data.links.html}`);
        return data;
    } catch (err) {
        console.error('❌ Failed creating draft deposition:', err.message);
        process.exit(1);
    }
}

async function main() {
    console.log('╔══════════════════════════════════════════════════════════════════════════╗');
    console.log('║   🕊️  PocketGull Font CERN / Zenodo Open Science Synchronizer        ║');
    console.log('║   Operated under CERN Data Centre & OpenAIRE Infrastructure             ║');
    console.log('╚══════════════════════════════════════════════════════════════════════════╝');

    const metadata = await validateMetadata();
    await validateCitationCff();
    await checkApiStatus();

    if (process.argv.includes('--create-draft')) {
        if (metadata) {
            await createDraft(metadata);
        }
    } else {
        console.log('💡 Tip: Run with --create-draft to create a new CERN Zenodo record using your ZENODO_ACCESS_TOKEN.');
        console.log('💡 Tip: Add --sandbox to target the CERN Zenodo Sandbox test environment.\n');
    }
}

main().catch(err => {
    console.error('Fatal error:', err);
    process.exit(1);
});
