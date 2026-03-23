# LLM Conveyors SDK - Comprehensive E2E Test Report

**Date:** 2026-03-23 20:17 UTC

**SDK Version:** 0.1.0

**Base URL:** https://api.llmconveyors.com/api/v1


## Summary


| Metric | Value |
|--------|-------|

| Total tests | 38 |

| Passed | 38 |

| Failed | 0 |

| Skipped | 0 |

| Pass rate | 100% |



## 1. Health Endpoints


### Test 1: Health check

- **Endpoint:** `GET /health`

- **Status:** PASS (0.8s)

- **Output:**
```json
{
  "status": "healthy",
  "timestamp": "2026-03-23T20:18:39.511Z",
  "uptime": 16389,
  "version": "1.0.0",
  "checks": {
    "mongo": "ok",
    "redis": "ok"
  },
  "memory": {
    "rss": 877,
    "heapUsed": 749,
    "heapTotal": 766
  }
}
```


### Test 2: Readiness

- **Endpoint:** `GET /health/ready`

- **Status:** PASS (0.3s)

- **Output:**
```json
{
  "ready": true
}
```


### Test 3: Liveness

- **Endpoint:** `GET /health/live`

- **Status:** PASS (0.3s)

- **Output:**
```json
{
  "alive": true
}
```


## 2. Settings Endpoints


### Test 4: Get profile

- **Endpoint:** `GET /settings/profile`

- **Status:** PASS (0.3s)

- **Output:**
```json
{
  "credits": 705.0,
  "tier": "byo",
  "byoKeyEnabled": true
}
```


### Test 5: Get preferences

- **Endpoint:** `GET /settings/preferences`

- **Status:** PASS (0.3s)

- **Output:**
```json
{
  "theme": "macchiato",
  "model": "flash",
  "autoSelectContacts": true
}
```


### Test 6: Get usage summary

- **Endpoint:** `GET /settings/usage-summary`

- **Input:**
```json
{
  "offset": 0,
  "limit": 50
}
```

- **Status:** PASS (0.3s)

- **Output:**
```json
{
  "totalCreditsUsed": 186.0,
  "totalGenerations": 33,
  "averageCreditsPerGeneration": 5.64
}
```


### Test 7: Get usage logs

- **Endpoint:** `GET /settings/usage-logs`

- **Input:**
```json
{
  "offset": 0,
  "limit": 5
}
```

- **Status:** PASS (0.3s)

- **Output:**
```json
{
  "logs": [
    {
      "id": "69c19ed7e592f5f0f7dc58a8",
      "timestamp": "2026-03-23T20:13:11.869Z",
      "type": "standard",
      "model": "gemini-3.1-pro-preview",
      "context": "job-hunter",
      "sessionId": "7528bc9a-0c06-4c24-819f-8251cf00cbf5",
      "jobId": "84",
      "tokens": {
        "promptTokens": 40654,
        "candidatesTokens": 18058,
        "totalTokens": 58712
      },
      "cost": {
        "totalCredits": 0,
        "providerCostUsd": 0.23139750000000003
      },
      "tier": "byo",
      "byoKey": true
    },
    {
      "id": "69c19e3de592f5f0f7dc5789",
      "timestamp": "2026-03-23T20:10:37.077Z",
      "type": "standard",
      "model": "gemini-3-flash-preview",
      "context": "resume-parse",
      "tokens": {
        "promptTokens": 479,
        "candidatesTokens": 1326,
        "totalTokens": 1805
      },
      "cost": {
        "totalCredits": 0,
        "providerCostUsd": 0.0042175
      },
      "tier": "byo",
      "byoKey": true
    },
    {
      "id": "69c19d27e592f5f0f7dc556e",
      "timestamp": "2026-03-23T20:05:59.090Z",
      "type": "standard",
      "model": "gemini-3-flash-preview",
      "context": "resume-parse",
      "tokens": {
        "promptTokens": 479,
        "candidatesTokens": 1286,
        "totalTokens": 1765
      },
      "cost": {
        "totalCredits": 0,
        "providerCostUsd": 0.0040975000000000004
      },
      "tier": "byo",
      "byoKey": true
    },
    {
      "id": "69c198c7e592f5f0f7dc544a",
      "timestamp": "2026-03-23T19:47:19.324Z",
      "type": "standard",
      "model": "gemini-3.1-pro-preview",
      "context": "job-hunter",
      "sessionId": "a13ce44c-522e-487a-af02-9f9a9d81c557",
      "jobId": "83",
      "tokens": {
        "promptTokens": 36561,
        "candidatesTokens": 14469,
        "totalTokens": 51030
      },
      "cost": {
        "totalCredits": 0,
        "providerCostUsd": 0.19039124999999998
      },
      "tier": "byo",
      "byoKey": true
    },
    {
      "id": "69c196f3e592f5f0f7dc52c8",
      "timestamp": "2026-03-23T19:39:31.855Z",
      "type": "standard",
      "model": "gemini-3.1-pro-preview",
      "context": "job-hunter",
      "sessionId": "4c05c0bf-93b9-44d4-8a6a-4b2937899ef7",
      "jobId": "82",
      "tokens": {
        "promptTokens": 40020,
        "candidatesTokens": 17571,
        "totalTokens": 57591
      },
      "cost": {
        "totalCredits": 0,
        "providerCostUsd": 0.22573500000000002
      },
      "tier": "byo",
      "byoKey": true
    }
  ],
  "total": 33
}
```


### Test 8: List API keys

- **Endpoint:** `GET /settings/platform-api-keys`

- **Status:** PASS (0.3s)

- **Output:**
```json
[
  {
    "hash": "",
    "label": "package-testing",
    "scopes": [
      "jobs:read",
      "sales:read",
      "sessions:read",
      "settings:read",
      "webhook:read",
      "jobs:write",
      "sales:write",
      "sessions:write",
      "upload:write",
      "resume:write",
      "ats:write",
      "webhook:write",
      "resume:read"
    ],
    "createdAt": "2026-03-23T05:25:40.382Z",
    "expiresAt": null,
    "lastUsedAt": "2026-03-23T20:18:41.266Z",
    "key": null,
    "keyHash": "9b060e8250260545fea4ce913fcfae482a4384f34f2d7c9eae191a7838914143",
    "keyPrefix": "llmc_6be0928",
    "monthlyCreditsLimit": null,
    "isActive": true,
    "currentMonthUsage": {
      "creditsUsed": 0,
      "requestCount": 0
    }
  },
  {
    "hash": "",
    "label": "test",
    "scopes": [
      "jobs:read",
      "sales:read",
      "sessions:read",
      "settings:read",
      "jobs:write",
      "sales:write",
      "sessions:write",
      "upload:write",
      "resume:write",
      "ats:write"
    ],
    "createdAt": "2026-03-08T19:12:55.144Z",
    "expiresAt": null,
    "lastUsedAt": "2026-03-08T19:45:33.021Z",
    "key": null,
    "keyHash": "4caa761b5a36b6f4c8412e4a68d9ccb57ea4c9f1a4b041b88a09b9acc8b48702",
    "keyPrefix": "llmc_5ee48a9",
    "monthlyCreditsLimit": null,
    "isActive": true,
    "currentMonthUsage": {
      "creditsUsed": 0,
      "requestCount": 0
    }
  },
  {
    "hash": "",
    "label": "test",
    "scopes": [
      "jobs:read",
      "sales:read",
      "sessions:read",
      "settings:read",
      "jobs:write",
      "sales:write",
      "sessions:write",
      "upload:write",
      "resume:write",
      "ats:write"
    ],
    "createdAt": "2026-03-08T14:04:50.749Z",
    "expiresAt": null,
    "lastUsedAt": "2026-03-08T15:54:55.963Z",
    "key": null,
    "keyHash": "259f9b56a6dc9ec33dbef48d1bf4faf4bff05e1d74e108ed321a61d3a7576998",
    "keyPrefix": "llmc_dafa554",
    "monthlyCreditsLimit": null,
    "isActive": false,
    "currentMonthUsage": {
      "creditsUsed": 0,
      "requestCount": 0
    }
  }
]
```


### Test 9: Get BYO key status

- **Endpoint:** `GET /settings/api-key`

- **Status:** PASS (0.3s)

- **Output:**
```json
{
  "ok": true,
  "hasKey": true,
  "isEnabled": true,
  "maskedKey": "AIzaSy...Qfd4",
  "updatedAt": "2026-03-15T21:20:40.730Z"
}
```


### Test 10: Get webhook secret

- **Endpoint:** `GET /settings/webhook-secret`

- **Status:** PASS (0.3s)

- **Output:**
```json
{
  "secret": "8869e6bca51fbc265d45f7e34d68acf86e75bd0a8d01e8c6c27b6b4f66ee1dbf",
  "createdAt": "2026-03-23T19:23:10.336Z"
}
```


## 3. Sessions Endpoints


### Test 11: Session init

- **Endpoint:** `GET /sessions/init`

- **Status:** PASS (0.9s)

- **Output:**
```json
{
  "user": {
    "uid": "4d05c369-c48e-4e01-871c-718ec19c0869",
    "email": "ebenezerv99@gmail.com",
    "displayName": "Ebenezer Veeraraju",
    "photoURL": "https://lh3.googleusercontent.com/a-/ALV-UjUp5isYt-hPwlAczsb9I7_6Q4db75KJAxMF2k65chfLIUpevGFf=s96-c",
    "tier": "byo",
    "credits": 705,
    "isAdmin": true,
    "apiKeyConfig": {
      "isEnabled": true,
      "hasKey": true
    }
  },
  "sessions": [
    {
      "id": "699efae2-a4c8-4278-9492-d6e9ba436dcc",
      "userId": "4d05c369-c48e-4e01-871c-718ec19c0869",
      "createdAt": "2026-03-23T06:16:14.874Z",
      "updatedAt": "2026-03-23T06:26:10.343Z",
      "status": "completed",
      "metadata": {
        "agentType": "b2b-sales",
        "source": "api-key",
        "companyName": "Notion",
        "companyWebsite": "https://notion.so",
        "coldEmailGenerations": [
          {
            "generationId": "203cbbba-5901-415d-8c17-9447b2f0b167",
            "subject": "Workplace comfort in the new Soho hub",
            "body": "Hi,\n\nCongratulations on reaching 100 million users and opening your new EMEA hubs.\n\nWith your 3-day RTO mandate, ensuring spaces like the London Soho office are flawlessly comfortable is critical for employee satisfaction. Cosysense uses secure, plug-and-play sensors to dynamically optimize HVAC based on real-time human comfort. Operating on a completely private network\u2014meaning zero risk to Notion's IT\u2014we improve workplace experience while cutting energy emissions by up to 40% at zero upfront cost.\n\nWould you be open to a brief chat about optimizing your new offices?\n\nBest,\nEbenezer Veeraraju",
            "toAddress": "",
            "ccAddress": "akshay@makenotion.com",
            "ccName": "Akshay Kothari",
            "ccTitle": "Co-Founder",
            "content": "Subject: Workplace comfort in the new Soho hub\n\nHi,\n\nCongratulations on reaching 100 million users and opening your new EMEA hubs.\n\nWith your 3-day RTO mandate, ensuring spaces like the London Soho office are flawlessly comfortable is critical for employee satisfaction. Cosysense uses secure, plug-and-play sensors to dynamically optimize HVAC based on real-time human comfort. Operating on a completely private network\u2014meaning zero risk to Notion's IT\u2014we improve workplace experience while cutting energy emissions by up to 40% at zero upfront cost.\n\nWould you be open to a brief chat about optimizing your new offices?\n\nBest,\nEbenezer Veeraraju",
            "storageKey": "users/4d05c369-c48e-4e01-871c-718ec19c0869/sessions/699efae2-a4c8-4278-9492-d6e9ba436dcc/cold-email-203cbbba-5901-415d-8c17-9447b2f0b167-1774247170322.md",
            "status": "completed",
            "createdAt": "2026-03-23T06:26:10.345Z"
          }
        ]
      },
      "chatHistory": [
        {
          "id": "74b0013c-f135-43a7-aebe-b9de1458e284",
          "role": "user",
          "content": "[B2B Sales] Generation started via API",
          "timestamp": "2026-03-
... (truncated)
```


### Test 12: List sessions

- **Endpoint:** `GET /sessions`

- **Status:** PASS (0.4s)

- **Output:**
```json
[
  {
    "id": "699efae2-a4c8-4278-9492-d6e9ba436dcc",
    "userId": "4d05c369-c48e-4e01-871c-718ec19c0869",
    "status": "completed",
    "createdAt": "2026-03-23T06:16:14.874Z",
    "updatedAt": "2026-03-23T06:26:10.343Z",
    "metadata": {
      "agentType": "b2b-sales",
      "source": "api-key",
      "companyName": "Notion",
      "companyWebsite": "https://notion.so",
      "coldEmailGenerations": [
        {
          "generationId": "203cbbba-5901-415d-8c17-9447b2f0b167",
          "subject": "Workplace comfort in the new Soho hub",
          "body": "Hi,\n\nCongratulations on reaching 100 million users and opening your new EMEA hubs.\n\nWith your 3-day RTO mandate, ensuring spaces like the London Soho office are flawlessly comfortable is critical for employee satisfaction. Cosysense uses secure, plug-and-play sensors to dynamically optimize HVAC based on real-time human comfort. Operating on a completely private network\u2014meaning zero risk to Notion's IT\u2014we improve workplace experience while cutting energy emissions by up to 40% at zero upfront cost.\n\nWould you be open to a brief chat about optimizing your new offices?\n\nBest,\nEbenezer Veeraraju",
          "toAddress": "",
          "ccAddress": "akshay@makenotion.com",
          "ccName": "Akshay Kothari",
          "ccTitle": "Co-Founder",
          "content": "Subject: Workplace comfort in the new Soho hub\n\nHi,\n\nCongratulations on reaching 100 million users and opening your new EMEA hubs.\n\nWith your 3-day RTO mandate, ensuring spaces like the London Soho office are flawlessly comfortable is critical for employee satisfaction. Cosysense uses secure, plug-and-play sensors to dynamically optimize HVAC based on real-time human comfort. Operating on a completely private network\u2014meaning zero risk to Notion's IT\u2014we improve workplace experience while cutting energy emissions by up to 40% at zero upfront cost.\n\nWould you be open to a brief chat about optimizing your new offices?\n\nBest,\nEbenezer Veeraraju",
          "storageKey": "users/4d05c369-c48e-4e01-871c-718ec19c0869/sessions/699efae2-a4c8-4278-9492-d6e9ba436dcc/cold-email-203cbbba-5901-415d-8c17-9447b2f0b167-1774247170322.md",
          "status": "completed",
          "createdAt": "2026-03-23T06:26:10.345Z"
        }
      ]
    },
    "chatHistory": [
      {
        "id": "74b0013c-f135-43a7-aebe-b9de1458e284",
        "role": "user",
        "content": "[B2B Sales] Generation started via API",
        "timestamp": "2026-03-23T06:16:14.892Z",
        "level": "info",
        "payload": {
          "source": "api",
          "agentType": "b2b-sales",
          "apiKeyPrefix": "llmc_6be0928"
        }
      }
    ]
  },
  {
    "id": "c6abc1de-d0ee-4c1a-8b7e-b89bf2a62cc6",
    "userId": "4d05c369-c48e-4e01-871c-718ec19c0869",
    "status": "completed",
    "createdAt": "2026-03-23T05:38:21.170Z",
    "updatedAt": "2026-03-23T05:41:36.451Z",
    "metadata": {
      "agentType": "job-hunter",
      "s
... (truncated)
```


### Test 13: Create session

- **Endpoint:** `POST /sessions`

- **Input:**
```json
{}
```

- **Status:** PASS (0.3s)

- **Output:**
```json
{
  "id": "4a53ac9f-5099-4a78-b280-b6db40c8643a",
  "userId": "4d05c369-c48e-4e01-871c-718ec19c0869",
  "status": "active",
  "createdAt": "2026-03-23T20:18:43.771Z",
  "updatedAt": "2026-03-23T20:18:43.771Z",
  "metadata": {},
  "chatHistory": []
}
```


### Test 14: Get session

- **Endpoint:** `GET /sessions/4a53ac9f-5099-4a78-b280-b6db40c8643a`

- **Status:** PASS (0.3s)

- **Output:**
```json
{
  "id": "4a53ac9f-5099-4a78-b280-b6db40c8643a",
  "userId": "4d05c369-c48e-4e01-871c-718ec19c0869",
  "status": "active",
  "createdAt": "2026-03-23T20:18:43.771Z",
  "updatedAt": "2026-03-23T20:18:43.771Z",
  "metadata": null,
  "chatHistory": []
}
```


### Test 15: Hydrate session

- **Endpoint:** `GET /sessions/4a53ac9f-5099-4a78-b280-b6db40c8643a/hydrate`

- **Status:** PASS (0.3s)

- **Output:**
```json
{
  "session": {
    "id": "4a53ac9f-5099-4a78-b280-b6db40c8643a",
    "userId": "4d05c369-c48e-4e01-871c-718ec19c0869",
    "status": "active",
    "createdAt": "2026-03-23T20:18:43.771Z",
    "updatedAt": "2026-03-23T20:18:43.771Z",
    "metadata": null,
    "chatHistory": []
  },
  "artifacts": [],
  "generationLogs": [],
  "activeGeneration": null,
  "cvVersions": [],
  "coverLetterVersions": [],
  "coldEmailVersions": [],
  "atsVersions": []
}
```


### Test 16: Append log

- **Endpoint:** `POST /sessions/4a53ac9f-5099-4a78-b280-b6db40c8643a/log`

- **Input:**
```json
{
  "role": "user",
  "content": "Test log entry from SDK E2E test"
}
```

- **Status:** PASS (0.3s)

- **Output:**
```json
"null (204 No Content)"
```


### Test 17: Delete session

- **Endpoint:** `DELETE /sessions/4a53ac9f-5099-4a78-b280-b6db40c8643a`

- **Status:** PASS (0.3s)

- **Output:**
```json
"null (204 No Content)"
```


## 4. Resume Endpoints


### Test 18: List themes

- **Endpoint:** `GET /resume/themes`

- **Status:** PASS (0.3s)

- **Output:**
```json
[
  {
    "name": "even",
    "displayName": "Even",
    "description": "Clean, modern, flat design with excellent markdown support",
    "supportsMarkdown": true
  },
  {
    "name": "stackoverflow",
    "displayName": "Stack Overflow",
    "description": "Developer-focused layout inspired by Stack Overflow",
    "supportsMarkdown": false
  },
  {
    "name": "class",
    "displayName": "Class",
    "description": "Self-contained design with i18n support",
    "supportsMarkdown": true
  },
  {
    "name": "professional",
    "displayName": "Professional",
    "description": "Modern typography with a clean professional look",
    "supportsMarkdown": true
  },
  {
    "name": "elegant",
    "displayName": "Elegant",
    "description": "Polished two-column layout with subtle color accents",
    "supportsMarkdown": false
  },
  {
    "name": "macchiato",
    "displayName": "Macchiato",
    "description": "Warm, minimalist design with a coffee-toned palette",
    "supportsMarkdown": false
  },
  {
    "name": "react",
    "displayName": "React",
    "description": "Modern React + Tailwind design with Markdown and i18n support",
    "supportsMarkdown": true
  },
  {
    "name": "academic",
    "displayName": "Academic",
    "description": "Academic serif design with small-caps headings and gold accents",
    "supportsMarkdown": false
  }
]
```


## 5. Agent Manifests


### Test 19: Job Hunter manifest

- **Endpoint:** `GET /agents/job-hunter/manifest`

- **Status:** PASS (0.3s)

- **Output:**
```json
{
  "agentType": "job-hunter",
  "label": "Job Hunter",
  "description": "Generate tailored CVs, cover letters, and cold emails for job applications",
  "skills": [
    "cv-generation",
    "ats-scoring",
    "cover-letter",
    "cold-email",
    "research",
    "contact-intel",
    "domain-bridge"
  ],
  "billing": {
    "minimumCredits": 30,
    "maximumCredits": 500
  },
  "capabilities": {
    "supportsPhasing": true,
    "hasArtifactVersioning": true
  },
  "inputFields": [
    {
      "name": "sessionId",
      "type": "string",
      "required": false,
      "autoLoaded": false,
      "description": "Session ID (auto-generated if omitted)"
    },
    {
      "name": "generationId",
      "type": "string",
      "required": false,
      "autoLoaded": false,
      "description": "Generation attempt ID (auto-generated if omitted)"
    },
    {
      "name": "masterResumeId",
      "type": "string",
      "required": false,
      "autoLoaded": false,
      "description": "Reference to a stored master CV \u2014 backend resolves to originalCV"
    },
    {
      "name": "tier",
      "type": "enum",
      "required": false,
      "autoLoaded": false,
      "description": "User billing tier"
    },
    {
      "name": "model",
      "type": "enum",
      "required": false,
      "autoLoaded": false,
      "description": "User-selected AI model preference"
    },
    {
      "name": "jobDescription",
      "type": "string",
      "required": false,
      "autoLoaded": false,
      "description": "Full job description text to tailor the CV and cover letter against"
    },
    {
      "name": "originalCV",
      "type": "string",
      "required": false,
      "autoLoaded": true,
      "description": "Raw text of the user's current CV/resume \u2014 auto-loaded if omitted"
    },
    {
      "name": "extensiveCV",
      "type": "string",
      "required": false,
      "autoLoaded": true,
      "description": "Comprehensive master CV \u2014 auto-loaded if omitted"
    },
    {
      "name": "cvStrategy",
      "type": "string",
      "required": false,
      "autoLoaded": true,
      "description": "User instructions for how to tailor the CV \u2014 auto-loaded if omitted"
    },
    {
      "name": "companyName",
      "type": "string",
      "required": true,
      "autoLoaded": false,
      "description": "Name of the target company"
    },
    {
      "name": "jobTitle",
      "type": "string",
      "required": true,
      "autoLoaded": false,
      "description": "Title of the target position"
    },
    {
      "name": "companyWebsite",
      "type": "string",
      "required": true,
      "autoLoaded": false,
      "description": "URL of the target company website for research"
    },
    {
      "name": "contactName",
      "type": "string",
      "required": false,
      "autoLoaded": false,
      "description": "Name of the hiring manager or contact person"
    },
    {
      "name": "contactTitle",
      "type": "string",
      "required": 
... (truncated)
```


### Test 20: B2B Sales manifest

- **Endpoint:** `GET /agents/b2b-sales/manifest`

- **Status:** PASS (0.3s)

- **Output:**
```json
{
  "agentType": "b2b-sales",
  "label": "B2B Sales",
  "description": "Generate personalized sales outreach for B2B prospecting",
  "skills": [
    "research",
    "contact-intel",
    "cold-email"
  ],
  "billing": {
    "minimumCredits": 50,
    "maximumCredits": 500
  },
  "capabilities": {
    "supportsPhasing": false,
    "hasArtifactVersioning": false
  },
  "inputFields": [
    {
      "name": "sessionId",
      "type": "string",
      "required": false,
      "autoLoaded": false,
      "description": "Session ID (auto-generated if omitted)"
    },
    {
      "name": "generationId",
      "type": "string",
      "required": false,
      "autoLoaded": false,
      "description": "Generation attempt ID (auto-generated if omitted)"
    },
    {
      "name": "masterResumeId",
      "type": "string",
      "required": false,
      "autoLoaded": false,
      "description": "Reference to a stored master CV \u2014 backend resolves to originalCV"
    },
    {
      "name": "tier",
      "type": "enum",
      "required": false,
      "autoLoaded": false,
      "description": "User billing tier"
    },
    {
      "name": "model",
      "type": "enum",
      "required": false,
      "autoLoaded": false,
      "description": "User-selected AI model preference"
    },
    {
      "name": "companyName",
      "type": "string",
      "required": true,
      "autoLoaded": false,
      "description": "Target company name"
    },
    {
      "name": "companyWebsite",
      "type": "string",
      "required": true,
      "autoLoaded": false,
      "description": ""
    },
    {
      "name": "userCompanyContext",
      "type": "string",
      "required": false,
      "autoLoaded": true,
      "description": "Background about the user's company for personalization"
    },
    {
      "name": "targetCompanyContext",
      "type": "string",
      "required": false,
      "autoLoaded": false,
      "description": "Pre-fetched target company context to override research"
    },
    {
      "name": "contactName",
      "type": "string",
      "required": false,
      "autoLoaded": false,
      "description": "Specific contact person to target"
    },
    {
      "name": "contactTitle",
      "type": "string",
      "required": false,
      "autoLoaded": false,
      "description": "Job title of the target contact"
    },
    {
      "name": "contactEmail",
      "type": "string",
      "required": false,
      "autoLoaded": false,
      "description": "Email of the target contact"
    },
    {
      "name": "salesStrategy",
      "type": "string",
      "required": false,
      "autoLoaded": true,
      "description": "User instructions for the sales approach"
    },
    {
      "name": "reconStrategy",
      "type": "string",
      "required": false,
      "autoLoaded": true,
      "description": "User instructions for research focus areas"
    },
    {
      "name": "companyResearch",
      "type": "string",
      "required": false,
      "autoLoaded": false,
... (truncated)
```


## 6. Shares Endpoints


### Test 21: List shares (stats)

- **Endpoint:** `GET /shares/stats`

- **Status:** PASS (0.3s)

- **Output:**
```json
[]
```


## 7. Referral Endpoints


### Test 22: Get referral stats

- **Endpoint:** `GET /referral/stats`

- **Status:** PASS (0.3s)

- **Output:**
```json
{
  "referralCode": "3A4J7E6F",
  "isVanityCode": false,
  "totalReferrals": 0,
  "pendingReferrals": 0,
  "completedReferrals": 0,
  "totalCreditsEarned": 0,
  "remainingThisYear": 15,
  "referrals": []
}
```


### Test 23: Get referral code

- **Endpoint:** `GET /referral/code`

- **Status:** PASS (0.3s)

- **Output:**
```json
{
  "code": "3A4J7E6F"
}
```


## 8. Privacy Endpoints


### Test 24: List consents

- **Endpoint:** `GET /privacy/consents`

- **Status:** PASS (0.3s)

- **Output:**
```json
[]
```


## 9. ATS Scoring


### Test 25: Score resume

- **Endpoint:** `POST /ats/score`

- **Input:**
```json
{
  "resumeText": "John Doe\nSenior Software Engineer | 10 Years Experience\n\nSKILLS: Python, TypeScript, React, Node.js, AWS, Docker, Kubernetes, PostgreSQL, MongoDB, Redis, GraphQL, REST APIs, CI/CD, Terraform\n\nEXPERIENCE:\nStaff Engineer at Amazon Web Services (2020-2026)\n- Led team of 8 engineers building real-time data pipelines\n- Reduced infrastructure costs by 40% through Kubernetes optimization\n- Designed microservices architecture serving 10M+ daily requests\n\nSenior Engineer at Stripe (2018-2020)\n- Built payment processing APIs handling $1B+ annual volume\n- Implemented automated testing reducing bugs by 60%\n\nEDUCATION: MS Computer Science, MIT (2016)\nBS Computer Science, Stanford (2014)",
  "jobDescription": "Senior Software Engineer - AI Platform\n\nWe're looking for an experienced engineer to build AI-powered tools. Requirements:\n- 5+ years experience with Python and TypeScript\n- Experience with cloud services (AWS/GCP) and containerization\n- Strong understanding of distributed systems and microservices\n- Experience with ML/AI infrastructure is a plus\n- Familiarity with CI/CD pipelines and infrastructure as code",
  "jobTitle": "Senior Software Engineer"
}
```

- **Status:** PASS (25.2s)

- **Output:**
```json
{
  "overallScore": 76,
  "grade": "B",
  "breakdown": {
    "keywordMatch": 59,
    "experienceRelevance": 61,
    "skillsCoverage": 66,
    "educationFit": 70,
    "formatQuality": 95
  },
  "matchedKeywords": [
    {
      "keyword": "python",
      "found": true,
      "confidence": 1,
      "matchChannel": "deterministic"
    },
    {
      "keyword": "typescript",
      "found": true,
      "confidence": 1,
      "matchChannel": "deterministic"
    },
    {
      "keyword": "amazon web services",
      "found": true,
      "confidence": 1,
      "matchChannel": "deterministic"
    },
    {
      "keyword": "docker",
      "found": true,
      "confidence": 1,
      "matchChannel": "deterministic"
    },
    {
      "keyword": "microservices",
      "found": true,
      "confidence": 1,
      "matchChannel": "deterministic"
    },
    {
      "keyword": "continuous integration",
      "found": true,
      "confidence": 1,
      "matchChannel": "deterministic"
    },
    {
      "keyword": "infrastructure as code",
      "found": true,
      "confidence": 0.8,
      "matchChannel": "taxonomy-rel"
    },
    {
      "keyword": "Strong understanding of distributed systems",
      "found": true,
      "confidence": 0.9,
      "matchChannel": "llm-semantic",
      "context": "microservices",
      "synonymUsed": "semantic equivalence"
    }
  ],
  "missingKeywords": [
    "google cloud platform",
    "distributed computing",
    "ML infrastructure",
    "AI infrastructure"
  ],
  "suggestions": [
    "Reformat your Experience section to ensure it is ATS-parsable. Use a standard format with clear job titles, company names, and date ranges (e.g., 'Month YYYY - Month YYYY') for each role.",
    "Integrate the missing required keywords 'Google Cloud Platform' and 'distributed computing' into your resume. Add them to your Skills section and, if applicable, describe how you used them in your Experience bullet points.",
    "Explicitly state your years of experience with key technologies mentioned in the job description, such as Python and TypeScript. You can add a 'Summary' section at the top to state 'Software Engineer with 5+ years of experience in Python and TypeScript'.",
    "Strengthen your resume by explicitly adding the term 'Infrastructure as Code (IaC)' and mentioning any specific tools you've used (e.g., Terraform, CloudFormation), as this was only inferred by the system."
  ],
  "semanticInsights": {
    "equivalentExperience": [
      {
        "requirement": "Strong understanding of distributed systems",
        "evidenceInResume": "microservices",
        "confidence": 0.9
      }
    ],
    "overallFitNarrative": "The candidate presents a mixed profile with a solid foundation in key required technologies like Python, AWS, Docker, and microservices. The resume effectively showcases impact through strong builder verbs (designed, built) and quantified metrics (Reduced costs by 40%). However, significant gaps exist, including missing requir
... (truncated)
```


## 10. Upload Endpoints


### Test 26: Upload job text

- **Endpoint:** `POST /upload/job-text`

- **Input:**
```json
{
  "text": "Senior Software Engineer - AI Platform at Anthropic\n\nAbout the role:\nWe're building the next generation of AI safety tools. You'll work on infrastructure powering Claude.\n\nRequirements:\n- 5+ years Python/TypeScript\n- Cloud infrastructure experience\n- Strong systems design skills\n\nLocation: San Francisco\nEmail: careers@anthropic.com"
}
```

- **Status:** PASS (5.1s)

- **Output:**
```json
{
  "jobDescription": "About the role: We're building the next generation of AI safety tools. You'll work on infrastructure powering Claude. Requirements: - 5+ years Python/TypeScript - Cloud infrastructure experience - Strong systems design skills Location: San Francisco Email: careers@anthropic.com",
  "companyName": "Anthropic",
  "jobTitle": "Senior Software Engineer - AI Platform",
  "companyWebsite": "https://www.anthropic.com",
  "wasUrl": false,
  "jobUrl": "",
  "emailAddresses": [],
  "metadata": {
    "city": "San Francisco",
    "country": "USA",
    "keywords": [
      "AI",
      "Software Engineer",
      "Python",
      "TypeScript",
      "Cloud infrastructure",
      "Systems design",
      "Anthropic",
      "Claude"
    ],
    "isRemote": false,
    "groundedExtraction": null
  },
  "processed": true,
  "degraded": false
}
```


## 11. Job Hunter — Full Generate + Stream Workflow


### Test 27: Generate (job-hunter)

- **Endpoint:** `POST /agents/job-hunter/generate`

- **Input:**
```json
{
  "companyName": "Anthropic",
  "jobTitle": "Senior Software Engineer",
  "companyWebsite": "https://anthropic.com",
  "contactEmail": "careers@anthropic.com",
  "genericEmail": "hello@anthropic.com",
  "jobSourceUrl": "https://anthropic.com/careers",
  "jobDescription": "Senior Software Engineer for AI safety research tools. 5+ years Python/TypeScript, distributed systems, ML infrastructure.",
  "autoSelectContacts": true,
  "skipResearchCache": true
}
```

- **Status:** PASS (6.4s)

- **Output:**
```json
{
  "jobId": "85",
  "generationId": "89ac0b0e-ab14-4e9a-95dc-d8caaec3b854",
  "sessionId": "4cd5ad58-408b-426a-80c6-6e74b6e08c32",
  "status": "queued",
  "streamUrl": "/api/v1/stream/generation/89ac0b0e-ab14-4e9a-95dc-d8caaec3b854"
}
```


### Test 28: SSE Stream

- **Endpoint:** `GET /stream/generation/89ac0b0e-ab14-4e9a-95dc-d8caaec3b854`

- **Events received:**

```

[Research] 5% - Looking up Anthropic

[log:info] Research: Looking up Anthropic

[heartbeat]

[heartbeat]

[heartbeat]

[heartbeat]

[heartbeat]

[heartbeat]

[heartbeat]

[heartbeat]

[heartbeat]

[heartbeat]

[heartbeat]

[Research] 35% - Compiling findings

[log:info] Research: Compiling findings

[heartbeat]

[Research] 38% - Research complete

[log:success] Research: Research complete

[ATS Pre-Score] 46% - Analyzing resume gaps

[log:info] ATS Pre-Score: Analyzing resume gaps

[Domain Bridge] 49% - Analyzing skill transferability

[log:info] Domain Bridge: Analyzing skill transferability

[Domain Bridge] 49% - moderate domain gap: 6 skill mappings, 5 transferable

[log:success] Domain Bridge: moderate domain gap: 6 skill mappings, 5 transferable

[heartbeat]

[heartbeat]

[ATS Pre-Score] 48% - Current score: 68/100 (C)

[log:success] ATS Pre-Score: Current score: 68/100 (C)

[CV Generation] 50% - Tailoring resume for Anthropic

[log:info] CV Generation: Tailoring resume for Anthropic

[CV Generation] 50% - Generating tailored resume

[log:info] CV Generation: Generating tailored resume

[heartbeat]

[heartbeat]

[heartbeat]

[heartbeat]

[heartbeat]

[heartbeat]

[CV Generation] 65% - Building PDF

[log:info] CV Generation: Building PDF

[heartbeat]

[CV Generation] 85% - Reviewing changes

[log:info] CV Generation: Reviewing changes

[CV Generation] 90% - Resume ready (3 pages)

[log:success] CV Generation: Resume ready (3 pages)

[ATS Scoring] 77% - Using saved ATS score

[log:info] ATS Scoring: Using saved ATS score

[ATS Scoring] 80% - Scoring optimized resume

[log:info] ATS Scoring: Scoring optimized resume

[ATS Scoring] 82% - Score: 68 → 89 (+21)

[log:success] ATS Scoring: Score: 68 → 89 (+21)

[Cover Letter] 80% - Writing cover letter

[log:info] Cover Letter: Writing cover letter

[heartbeat]

[heartbeat]

[Cover Letter] 90% - Cover letter ready

[log:success] Cover Letter: Cover letter ready

[Finalizing] 95% - 4 document(s) ready

[log:success] Finalizing: 4 document(s) ready

[COMPLETE] success=True, artifacts=4, awaitingInput=None

```

- **Duration:** 351.3s

- **Event counts:** {"ProgressEvent": 18, "LogEvent": 18, "HeartbeatEvent": 23, "CompleteEvent": 1}

- **Status:** PASS


## 12. Status Polling + Artifact Retrieval


### Test 28: Get status (with artifacts)

- **Endpoint:** `GET /agents/job-hunter/status/85`

- **Input:**
```json
{
  "include": "logs,artifacts"
}
```

- **Status:** PASS (0.6s)

- **Output:**
```json
{
  "jobId": "85",
  "generationId": "89ac0b0e-ab14-4e9a-95dc-d8caaec3b854",
  "sessionId": "4cd5ad58-408b-426a-80c6-6e74b6e08c32",
  "agentType": "job-hunter",
  "status": "completed",
  "progress": 100,
  "currentStep": "",
  "failedReason": null,
  "interactionData": null,
  "logs": [
    {
      "content": "Starting generation",
      "level": "info",
      "timestamp": "2026-03-23T20:19:23.686Z"
    },
    {
      "content": "Research: Looking up Anthropic",
      "level": "info",
      "timestamp": "2026-03-23T20:19:23.715Z"
    },
    {
      "content": "Research: Compiling findings",
      "level": "info",
      "timestamp": "2026-03-23T20:22:09.011Z"
    },
    {
      "content": "Research: Research complete",
      "level": "success",
      "timestamp": "2026-03-23T20:22:35.871Z"
    },
    {
      "content": "ATS Pre-Score: Analyzing resume gaps",
      "level": "info",
      "timestamp": "2026-03-23T20:22:35.878Z"
    },
    {
      "content": "Domain Bridge: Analyzing skill transferability",
      "level": "info",
      "timestamp": "2026-03-23T20:22:35.878Z"
    },
    {
      "content": "Domain Bridge: moderate domain gap: 6 skill mappings, 5 transferable",
      "level": "success",
      "timestamp": "2026-03-23T20:22:35.884Z"
    },
    {
      "content": "ATS Pre-Score: Current score: 68/100 (C)",
      "level": "success",
      "timestamp": "2026-03-23T20:22:57.746Z"
    },
    {
      "content": "CV Generation: Tailoring resume for Anthropic",
      "level": "info",
      "timestamp": "2026-03-23T20:22:57.755Z"
    },
    {
      "content": "CV Generation: Generating tailored resume",
      "level": "info",
      "timestamp": "2026-03-23T20:22:57.762Z"
    },
    {
      "content": "CV Generation: Building PDF",
      "level": "info",
      "timestamp": "2026-03-23T20:24:37.883Z"
    },
    {
      "content": "CV Generation: Reviewing changes",
      "level": "info",
      "timestamp": "2026-03-23T20:24:40.000Z"
    },
    {
      "content": "CV Generation: Resume ready (3 pages)",
      "level": "success",
      "timestamp": "2026-03-23T20:24:46.520Z"
    },
    {
      "content": "ATS Scoring: Using saved ATS score",
      "level": "info",
      "timestamp": "2026-03-23T20:24:46.535Z"
    },
    {
      "content": "ATS Scoring: Scoring optimized resume",
      "level": "info",
      "timestamp": "2026-03-23T20:24:46.543Z"
    },
    {
      "content": "ATS Scoring: Score: 68 \u2192 89 (+21)",
      "level": "success",
      "timestamp": "2026-03-23T20:24:49.679Z"
    },
    {
      "content": "Cover Letter: Writing cover letter",
      "level": "info",
      "timestamp": "2026-03-23T20:24:49.683Z"
    },
    {
      "content": "Cover Letter: Cover letter ready",
      "level": "success",
      "timestamp": "2026-03-23T20:25:14.884Z"
    },
    {
      "content": "Finalizing: 4 document(s) ready",
      "level": "success",
      "timestamp": "2026-03-23T20:25:14.895Z"
    }
  ],
  "artifacts": [
    {
      "storageKey": "ses
... (truncated)
```


### Artifacts from generation

- **Count:** 4

- **Details:**

```json

Artifact 1:
{
  "id": "company-research-89ac0b0e-ab14-4e9a-95dc-d8caaec3b854",
  "type": "company-research",
  "storageKey": "sessions/4cd5ad58-408b-426a-80c6-6e74b6e08c32/89ac0b0e-ab14-4e9a-95dc-d8caaec3b854/company-research/company-research.md",
  "downloadUrl": "sessions/4cd5ad58-408b-426a-80c6-6e74b6e08c32/89ac0b0e-ab14-4e9a-95dc-d8caaec3b854/company-research/company-research.md",
  "mimeType": "text/plain",
  "payload": {
    "content": "# Research Report on Anthropic: Strategic Insights for Senior Software Engineering Candidates\n\nResearch suggests that Anthropic is currently positioning itself as a dominant force in the enterprise artificial intelligence sector, balancing rapid commercial growth with a foundational commitment to AI safety. It seems likely that the company's distinct corporate structure and rigorous ethical frameworks set it apart from its primary competitors. The evidence leans toward Anthropic capturing a significant majority of new enterprise software expenditures, driven by highly capable models and developer-centric tools. \n\n*   **Market Leadership:** Evidence suggests that Anthropic has recently overtaken major competitors in enterprise LLM market share, particularly in coding and agentic workflows.\n*   **Financial Hypergrowth:** It appears that the organization is experiencing unprecedented financial scaling, with reported run-rate revenues reaching $14 billion following a historic $30 billion Series G funding round.\n*   **Safety-Centric Culture:** Rese
  ... (truncated)


Artifact 2:
{
  "id": "cv-89ac0b0e-ab14-4e9a-95dc-d8caaec3b854",
  "type": "cv",
  "storageKey": "sessions/4cd5ad58-408b-426a-80c6-6e74b6e08c32/89ac0b0e-ab14-4e9a-95dc-d8caaec3b854/cv/resume.json",
  "pdfStorageKey": "sessions/4cd5ad58-408b-426a-80c6-6e74b6e08c32/89ac0b0e-ab14-4e9a-95dc-d8caaec3b854/cv/resume.pdf",
  "downloadUrl": "sessions/4cd5ad58-408b-426a-80c6-6e74b6e08c32/89ac0b0e-ab14-4e9a-95dc-d8caaec3b854/cv/resume.pdf",
  "mimeType": "application/pdf",
  "payload": {
    "resume": {
      "basics": {
        "name": "Ebenezer Isaac",
        "label": "Software Engineer | Full-Stack Developer (Python/TypeScript)",
        "image": "",
        "url": "https://ebenezer-isaac.com",
        "summary": "Software Engineer with over 5 years of combined professional and freelance experience building scalable applications, developer tooling, and ML infrastructure. Demonstrated expertise in Python and TypeScript, with a focus on engineering distributed systems and robust data pipelines. Developed custom static analysis tools that reduced bug-triage time by 70% at IBM, and engineered an end-to-end machine learning data pipeline for facial classification.",
        "location": {
          "city": "London",
          "countryCode": "UK",
          "region": "",
          "address": "",
          "postalCode": "London"
        },
        "email": "ebnezr.isaac@gmail.com",
        "phone": "+44 75010 53232",
        "profiles": [
          {
            "network": "LinkedIn",
            "user
  ... (truncated)


Artifact 3:
{
  "id": "ats-comparison-89ac0b0e-ab14-4e9a-95dc-d8caaec3b854",
  "type": "ats-comparison",
  "payload": {
    "before": {
      "overallScore": 68,
      "grade": "C",
      "breakdown": {
        "keywordMatch": 52,
        "experienceRelevance": 41,
        "skillsCoverage": 60,
        "educationFit": 70,
        "formatQuality": 85
      },
      "matchedKeywords": [
        {
          "keyword": "python",
          "found": true,
          "confidence": 1,
          "matchChannel": "deterministic"
        },
        {
          "keyword": "typescript",
          "found": true,
          "confidence": 1,
          "matchChannel": "deterministic"
        },
        {
          "keyword": "software development",
          "found": true,
          "confidence": 1,
          "matchChannel": "deterministic"
        }
      ],
      "missingKeywords": [
        "distributed computing",
        "ML infrastructure"
      ],
      "suggestions": [
        "Restructure your 'Experience' section with a standard format (Job Title, Company, Dates, Bullet Points) to ensure it can be correctly parsed by ATS. This is the most critical issue as your entire work history is currently not being evaluated.",
        "Incorporate the missing required keywords 'distributed computing' and 'ML infrastructure' into your Skills and Experience sections. Detail projects or tasks where you utilized these technologies to align with the core requirements of the AI role.",
        "Once your experienc
  ... (truncated)


Artifact 4:
{
  "id": "cover-letter-89ac0b0e-ab14-4e9a-95dc-d8caaec3b854",
  "type": "cover-letter",
  "storageKey": "sessions/4cd5ad58-408b-426a-80c6-6e74b6e08c32/89ac0b0e-ab14-4e9a-95dc-d8caaec3b854/cover-letter/cover-letter.txt",
  "downloadUrl": "sessions/4cd5ad58-408b-426a-80c6-6e74b6e08c32/89ac0b0e-ab14-4e9a-95dc-d8caaec3b854/cover-letter/cover-letter.txt",
  "mimeType": "text/plain",
  "payload": {
    "content": "23 March 2026\n\nDear Hiring Manager,\n\nI am writing to apply for the Senior Software Engineer position on the AI safety research tools team at Anthropic. As an engineer who values a high trust and low ego culture, I am deeply inspired by your commitment to building reliable and steerable AI through innovations like Constitutional AI. With your recent Series G funding and rapid infrastructure scaling to support the Claude model family, you need pragmatic builders who can do the simple thing that works to accelerate your safety research.\n\nYour researchers require robust and token efficient tooling to bridge the gap between frontier science and production grade engineering. Throughout my career, I have focused on building tools that multiply developer efficiency using Python and TypeScript. At IBM, I developed a static analysis tool in Node.js that parsed application dependency graphs and reduced bug triage time by 70 percent. I also authored targeted Python scripts that automated complex infrastructure checks, cutting project planning time by one full week and deriskin
  ... (truncated)


```


### Test 29: Hydrate generation session

- **Endpoint:** `GET /sessions/4cd5ad58-408b-426a-80c6-6e74b6e08c32/hydrate`

- **Status:** PASS (0.4s)

- **Output:**
```json
{
  "session": {
    "id": "4cd5ad58-408b-426a-80c6-6e74b6e08c32",
    "userId": "4d05c369-c48e-4e01-871c-718ec19c0869",
    "status": "completed",
    "createdAt": "2026-03-23T20:19:23.682Z",
    "updatedAt": "2026-03-23T20:25:14.936Z",
    "metadata": {
      "agentType": "job-hunter",
      "source": "api-key",
      "companyName": "Anthropic",
      "jobTitle": "Senior Software Engineer",
      "companyWebsite": "https://anthropic.com",
      "mode": "standard",
      "jobDescription": "Senior Software Engineer for AI safety research tools. 5+ years Python/TypeScript, distributed systems, ML infrastructure.",
      "rawJobInput": "Senior Software Engineer for AI safety research tools. 5+ years Python/TypeScript, distributed systems, ML infrastructure.",
      "cvGenerations": [
        {
          "generationId": "89ac0b0e-ab14-4e9a-95dc-d8caaec3b854",
          "theme": "macchiato",
          "pageCount": 3,
          "changeSummary": "- Updated professional label and summary to emphasize 5+ years of experience and a focus on Full-Stack development (Python/TypeScript), distributed systems, and ML infrastructure.\n- Refined the **IBM Web Engineer** role to focus on static analysis, dependency graphs, and Python-driven infrastructure automation, replacing previous mentions of UI modernization and mentoring.\n- Restructured the **Skills** section, adding new categories for \"Distributed Systems & Cloud,\" \"ML & Data Infrastructure,\" and \"Developer Tools\" while removing the dedicated \"Hardware & Microprocessors\" section.\n- Added two new technical projects: **Intoxicated Face Identification** (ML data pipeline) and **mediamtx-onvif-wsdd** (headless RTSP proxy).\n- Rebranded and updated the **Fingerprint Attendance System** project to the **Cerberus Distributed Attendance System**, focusing on its distributed computing architecture and biometric data caching.\n- Updated work highlights to prioritize technical keywords like **TypeScript**, **distributed state**, and **data structures** over previous mentions of SEO and UI layouts.\n- Minor edits to the **Jatpoint** role to specify the use of TypeScript and the **Freelance** role to focus on backend architecture over SEO.",
          "status": "completed",
          "createdAt": "2026-03-23T20:25:14.935Z",
          "storageKey": "sessions/4cd5ad58-408b-426a-80c6-6e74b6e08c32/89ac0b0e-ab14-4e9a-95dc-d8caaec3b854/cv/resume.json",
          "pdfStorageKey": "sessions/4cd5ad58-408b-426a-80c6-6e74b6e08c32/89ac0b0e-ab14-4e9a-95dc-d8caaec3b854/cv/resume.pdf"
        }
      ],
      "theme": "macchiato",
      "coverLetterGenerations": [
        {
          "generationId": "89ac0b0e-ab14-4e9a-95dc-d8caaec3b854",
          "status": "completed",
          "createdAt": "2026-03-23T20:25:14.935Z",
          "storageKey": "sessions/4cd5ad58-408b-426a-80c6-6e74b6e08c32/89ac0b0e-ab14-4e9a-95dc-d8caaec3b854/cover-letter/cover-letter.txt",
          "toAddress": "careers@anthropic.com"
        }
      ],
 
... (truncated)
```


**Hydration details:**

- Artifacts: 4

- Generation logs: 1

- CV versions: 1

- Cover letter versions: 1

- Cold email versions: 0

- ATS versions: 1


## 13. Artifact Download


### Test 30: Download artifact (company-research)

- **Endpoint:** `GET /sessions/4cd5ad58-408b-426a-80c6-6e74b6e08c32/download?key=sessions/4cd5ad58-408b-426a-80c6-6e74b6e08c32/89ac0b0e-ab14-4e9a-95dc-d8caaec3b854/company-research/company-research.md`

- **Input:**
```json
{
  "key": "sessions/4cd5ad58-408b-426a-80c6-6e74b6e08c32/89ac0b0e-ab14-4e9a-95dc-d8caaec3b854/company-research/company-research.md"
}
```

- **Status:** PASS (0.3s)

- **Output:**
```json
{
  "content": "# Research Report on Anthropic: Strategic Insights for Senior Software Engineering Candidates\n\nResearch suggests that Anthropic is currently positioning itself as a dominant force in the enterprise artificial intelligence sector, balancing rapid commercial growth with a foundational commitment to AI safety. It seems likely that the company's distinct corporate structure and rigorous ethical frameworks set it apart from its primary competitors. The evidence leans toward Anthropic capturing a significant majority of new enterprise software expenditures, driven by highly capable models and developer-centric tools. \n\n*   **Market Leadership:** Evidence suggests that Anthropic has recently overtaken major competitors in enterprise LLM market share, particularly in coding and agentic workflows.\n*   **Financial Hypergrowth:** It appears that the organization is experiencing unprecedented financial scaling, with reported run-rate revenues reaching $14 billion following a historic $30 billion Series G funding round.\n*   **Safety-Centric Culture:** Research indicates that the company maintains a \"high-trust, low-ego\" environment where alignment with AI safety principles is heavily weighted in both engineering practices and hiring decisions.\n*   **Technical Complexity:** It is highly likely that engineers at Anthropic face frontier-level challenges in distributed systems, mechanistic interpretability, and performance optimization across diverse hardware accelerators.\n*   **Strategic Differentiation:** The company's reliance on Constitutional AI, combined with a diversified compute infrastructure, seems to provide structural and ethical advantages in the enterprise sector.\n\n### Organizational Context\nAnthropic operates at the frontier of artificial intelligence research and commercialization. Founded by former OpenAI researchers, the company is fundamentally structured around the goal of developing safe, steerable, and interpretable AI systems. This mission is not merely a theoretical exercise but is deeply integrated into their product development, engineering culture, and corporate governance.\n\n### Purpose of this Report\nThis document provides an exhaustive academic and strategic analysis of Anthropic, tailored specifically for a Senior Software Engineer preparing for the job application and interview process. By synthesizing the latest available data on company culture, financial growth, market positioning, technical pain points, and competitive differentiation, this report delivers actionable intelligence to optimize a curriculum vitae (CV) and cover letter.\n\n---\n\n## 1. Company Culture and Core Values\n\nTo successfully navigate the recruitment process at Anthropic, a candidate must demonstrate profound alignment with the organization's unique cultural ethos. Anthropic's culture is heavily defined by its founding narrative: the organization was established by researchers who prioritized a different, more cautious appro
... (truncated)
```

- **Size:** 0 bytes


### Test 31: Download artifact (cv)

- **Endpoint:** `GET /sessions/4cd5ad58-408b-426a-80c6-6e74b6e08c32/download?key=sessions/4cd5ad58-408b-426a-80c6-6e74b6e08c32/89ac0b0e-ab14-4e9a-95dc-d8caaec3b854/cv/resume.json`

- **Input:**
```json
{
  "key": "sessions/4cd5ad58-408b-426a-80c6-6e74b6e08c32/89ac0b0e-ab14-4e9a-95dc-d8caaec3b854/cv/resume.json"
}
```

- **Status:** PASS (0.3s)

- **Output:**
```json
{
  "content": "{\"basics\":{\"name\":\"Ebenezer Isaac\",\"label\":\"Software Engineer | Full-Stack Developer (Python/TypeScript)\",\"image\":\"\",\"url\":\"https://ebenezer-isaac.com\",\"summary\":\"Software Engineer with over 5 years of combined professional and freelance experience building scalable applications, developer tooling, and ML infrastructure. Demonstrated expertise in Python and TypeScript, with a focus on engineering distributed systems and robust data pipelines. Developed custom static analysis tools that reduced bug-triage time by 70% at IBM, and engineered an end-to-end machine learning data pipeline for facial classification.\",\"location\":{\"city\":\"London\",\"countryCode\":\"UK\",\"region\":\"\",\"address\":\"\",\"postalCode\":\"London\"},\"email\":\"ebnezr.isaac@gmail.com\",\"phone\":\"+44 75010 53232\",\"profiles\":[{\"network\":\"LinkedIn\",\"username\":\"ebnezr-isaac\",\"url\":\"https://www.linkedin.com/in/ebnezr-isaac/\"},{\"network\":\"GitHub\",\"username\":\"ebenezer-isaac\",\"url\":\"https://github.com/ebenezer-isaac\"}]},\"work\":[{\"name\":\"Cosysense Ltd\",\"position\":\"IoT Intern\",\"startDate\":\"2026-01-07\",\"endDate\":\"2026-03-27\",\"summary\":\"Spearheaded frontend architecture and UI correctness for an internal administrative platform, integrating data from connected microprocessors.\",\"highlights\":[\"Built complex spatial mapping components using React Leaflet, managing distributed state for over 20 distinct IoT microprocessors and device contexts.\",\"Developed robust, self-contained interactive user interfaces utilizing Tailwind CSS, Vite, and ReactJS within an agile team.\",\"Translated complex data models into verifiable, robust UI components prioritizing scalable architecture and code maintainability.\",\"Integrated AWS Cognito to ensure robust identity management and secure credential handling across the client-side web application.\"]},{\"name\":\"Jatpoint\",\"position\":\"Full Stack Application Developer\",\"startDate\":\"2025-12-23\",\"endDate\":\"2026-02-25\",\"summary\":\"Lead Architect for the rapid 8-week end-to-end development of the platform's Phase 2 overhaul, demonstrating adaptability in high-pressure environments.\",\"highlights\":[\"Engineered a high-performance cross-platform frontend utilizing TypeScript and a scalable, cloud-native Node.js backend deployed on AWS.\",\"Implemented secure Stripe payment gateways and robust payment processing logic alongside a real-time digital reward redemption system.\",\"Architected a dynamic 3-axis radar chart visualization algorithm designed to compute and display user engagement in real time.\",\"Established automated deployment pipelines using GitHub Actions, ensuring consistent and verifiable releases to staging environments.\"]},{\"name\":\"IBM India Private Limited\",\"position\":\"Client-side Web Application Engineer\",\"startDate\":\"2023-11-01\",\"endDate\":\"2025-07-31\",\"summary\":\"Engineered robust web applications and automated 
... (truncated)
```

- **Size:** 0 bytes


### Test 32: Download artifact (cover-letter)

- **Endpoint:** `GET /sessions/4cd5ad58-408b-426a-80c6-6e74b6e08c32/download?key=sessions/4cd5ad58-408b-426a-80c6-6e74b6e08c32/89ac0b0e-ab14-4e9a-95dc-d8caaec3b854/cover-letter/cover-letter.txt`

- **Input:**
```json
{
  "key": "sessions/4cd5ad58-408b-426a-80c6-6e74b6e08c32/89ac0b0e-ab14-4e9a-95dc-d8caaec3b854/cover-letter/cover-letter.txt"
}
```

- **Status:** PASS (0.3s)

- **Output:**
```json
{
  "content": "23 March 2026\n\nDear Hiring Manager,\n\nI am writing to apply for the Senior Software Engineer position on the AI safety research tools team at Anthropic. As an engineer who values a high trust and low ego culture, I am deeply inspired by your commitment to building reliable and steerable AI through innovations like Constitutional AI. With your recent Series G funding and rapid infrastructure scaling to support the Claude model family, you need pragmatic builders who can do the simple thing that works to accelerate your safety research.\n\nYour researchers require robust and token efficient tooling to bridge the gap between frontier science and production grade engineering. Throughout my career, I have focused on building tools that multiply developer efficiency using Python and TypeScript. At IBM, I developed a static analysis tool in Node.js that parsed application dependency graphs and reduced bug triage time by 70 percent. I also authored targeted Python scripts that automated complex infrastructure checks, cutting project planning time by one full week and derisking deployment timelines. I bring this same pragmatic problem solving approach to resolving bottlenecks for research teams.\n\nThe scale of mechanistic interpretability research requires deep expertise in distributed systems and ML infrastructure. My hands on experience spans the full machine learning lifecycle. I engineered an end to end data pipeline for a facial classification project, handling everything from frame extraction and alignment to data augmentation and model training. Furthermore, I have architected distributed computing systems, such as the Cerberus platform, which coordinated state and tasks between remote edge clients and a central web application. This experience designing distributed systems to manage on demand data caching directly translates to the complex data pipelines required for your research infrastructure.\n\nI am eager to bring my five years of experience in Python and TypeScript to Anthropic to help build the scalable systems that empower your AI safety researchers. Thank you for your time and consideration. I look forward to discussing how my background aligns with your engineering needs.\n\nSincerely,\n\nEbenezer Isaac",
  "mimeType": "text/plain"
}
```

- **Size:** 0 bytes


## 14. Content Endpoints


### Test 33: Delete generation

- **Endpoint:** `DELETE /content/generations/89ac0b0e-ab14-4e9a-95dc-d8caaec3b854`

- **Input:**
```json
{
  "sessionId": "4cd5ad58-408b-426a-80c6-6e74b6e08c32"
}
```

- **Status:** PASS (0.3s)

- **Output:**
```json
"null (204 No Content)"
```


> Cleaned up session 4cd5ad58-408b-426a-80c6-6e74b6e08c32


## 15. Documents Endpoint


### Test 34: Download (invalid path raises FORBIDDEN)

- **Endpoint:** `GET /documents/download`

- **Input:**
```json
{
  "path": "nonexistent"
}
```

- **Status:** PASS (expected error)

- **Error Code:** `FORBIDDEN` (expected)

- **Error Message:** Access denied to this resource

- **SDK handled correctly:** Raised `ForbiddenError`


## 16. Logging Endpoint


### Test 35: Send log

- **Endpoint:** `POST /log`

- **Input:**
```json
{
  "level": "info",
  "message": "SDK E2E test log"
}
```

- **Status:** PASS (0.3s)

- **Output:**
```json
"null (204 No Content)"
```


### Test 36: Send log (invalid extra field raises VALIDATION_ERROR)

- **Endpoint:** `POST /log`

- **Input:**
```json
{
  "level": "info",
  "message": "test",
  "context": "extra_field"
}
```

- **Status:** PASS (expected error)

- **Error Code:** `VALIDATION_ERROR` (expected)

- **Error Message:** Invalid log entry

- **SDK handled correctly:** Raised `ValidationError`


## 17. Auth Endpoints


### Test 37: Export data (API key raises FORBIDDEN — session auth required)

- **Endpoint:** `GET /auth/export`

- **Status:** PASS (expected error)

- **Error Code:** `FORBIDDEN` (expected)

- **Error Message:** Account management requires session authentication — API keys are not permitted

- **SDK handled correctly:** Raised `ForbiddenError`
