# PocketGull Font Superfamily on Amazon Web Services (AWS)

Clinical sans-serif and fixed 600 UPM telemetry monospace fonts optimized for **AWS Lambda serverless PDF rendering**, **Amazon ECS / Fargate container workloads**, and **Amazon CloudFront edge delivery**.

---

## 1. AWS Lambda Font Layer (Headless PDF, Puppeteer & WeasyPrint)
AWS Lambda execution environments do not include desktop fonts by default. Serverless PDF generation functions (using Puppeteer, Chromium, Playwright, or WeasyPrint) fail with tofu boxes or ugly system fallbacks.

The pre-built Lambda layer is located at:
`distribution/aws/pocketgull-lambda-fonts.zip`

### Deploying the Layer via AWS CLI:
```bash
aws lambda publish-layer-version \
    --layer-name pocketgull-fonts \
    --description "PocketGull clinical and monospace fonts for Lambda report and PDF generation" \
    --zip-file fileb://distribution/aws/pocketgull-lambda-fonts.zip \
    --compatible-runtimes nodejs20.x nodejs22.x python3.11 python3.12 provided.al2023 \
    --compatible-architectures x86_64 arm64
```

### In Your Lambda Function (Node.js / Python):
When attached, the fonts automatically mount to `/opt/fonts/` with fontconfig pre-configured at `/opt/fontconfig/fonts.conf`:
```python
import os
# Point Fontconfig to the Lambda layer
os.environ["FONTCONFIG_PATH"] = "/opt/fontconfig"
```

---

## 2. Docker / Amazon ECS / AWS Fargate
Add PocketGull directly to your serverless container images:

```dockerfile
# Multi-stage font installation in Amazon Linux 2023 / Debian container
COPY --from=ghcr.io/pocketgull-app/pocketgull-font:latest /fonts/ttf/ /usr/share/fonts/truetype/pocketgull/
RUN fc-cache -f -v
```

---

## 3. Amazon CloudFront & S3 Webfont Edge Delivery
When serving PocketGull WOFF2 webfonts from an Amazon S3 bucket behind CloudFront, ensure CORS and immutable cache headers are configured:

```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["*"],
      "AllowedMethods": ["GET", "HEAD"],
      "AllowedHeaders": ["*"],
      "MaxAgeSeconds": 31536000
    }
  ]
}
```

CloudFront Response Headers Policy:
* `Cache-Control: public, max-age=31536000, immutable`
* `Access-Control-Allow-Origin: *`
