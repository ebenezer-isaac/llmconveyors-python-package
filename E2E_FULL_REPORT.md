# Extended E2E — 2026-03-23 20:51 UTC


## B2B Sales — Full Generate + Stream + Artifacts

  [1] PASS B2B Generate: {"jobId": "92", "generationId": "c1555b4b-8612-42b4-b0a2-38aa092516ed", "sessionId": "0f0757c5-6dd8-417d-ac0d-597c91ca916e", "status": "queued", "streamUrl": "/api/v1/stream/generation/c1555b4b-8612-42b4-b0a2-38aa092516ed"}
```
{
  "jobId": "92",
  "generationId": "c1555b4b-8612-42b4-b0a2-38aa092516ed",
  "sessionId": "0f0757c5-6dd8-417d-ac0d-597c91ca916e",
  "status": "queued",
  "streamUrl": "/api/v1/stream/generation/c1555b4b-8612-42b4-b0a2-38aa092516ed"
}
```


### SSE Stream for B2B Sales

    [Research] 10% - Deep research on Notion
    [log:info] Research: Deep research on Notion
    [Research] 15% - Researching Notion
    [log:info] Research: Researching Notion
    [Research] 90% - Notion research done
    [log:success] Research: Notion research done
    [Enrichment] 10% - Looking up undefined
    [log:info] Enrichment: Looking up undefined
    [Enrichment] 15% - Searching for contacts
    [log:info] Enrichment: Searching for contacts
    [Enrichment] 45% - Analyzing candidates
    [log:info] Enrichment: Analyzing candidates
    [Enrichment] 75% - Selecting best matches
    [log:info] Enrichment: Selecting best matches
    [Enrichment] 90% - Getting contact details
    [log:info] Enrichment: Getting contact details
    [Enrichment] 100% - Discovery complete
    [log:info] Enrichment: Discovery complete
    [Enrichment] 100% - No verified email found
    [log:warn] Enrichment: No verified email found
    [Person Research] 50% - Looking up Akshay Kothari
    [log:info] Person Research: Looking up Akshay Kothari
    [Email] 10% - Writing email to Notion
    [log:info] Email: Writing email to Notion
    [Email] 100% - Email ready
    [log:success] Email: Email ready
    [COMPLETE] success=True, artifacts=3

**Stream duration:** 481s | **Events:** {"ProgressEvent": 13, "LogEvent": 13, "HeartbeatEvent": 32, "CompleteEvent": 1}

### B2B Artifacts (3)

**Artifact 1: company-research**
```
# Deep Research Report: Strategic Analysis of Notion Labs, Inc. and Alignment Opportunities for Cosysense

**Key Points:**
*   Research suggests Notion is a dominant force in the productivity software market, transitioning from a workspace tool to a comprehensive AI agent platform.
*   The company's estimated annual recurring revenue (ARR) appears to have reached approximately $600 million by late 2025, largely driven by AI-enabled customers.
*   Evidence leans toward a current valuation of $11 billion, recently solidified by a $270 million secondary tender offer in early 2026.
*   Notion's physical footprint is expanding significantly; records indicate a recent 114,646-square-foot headquarters lease in San Francisco, presenting a substantial facility management profile.
*   It seems likely that as Notion prepares for a potential IPO, operational efficiency and Environmental, Social, and Governance (ESG) compliance will become increasingly critical priorities.

**Introduction**
The following comprehensive analysis examines Notion Labs, Inc. (operating as Notion), a pioneering software-as-a-service (SaaS) enterprise that has reshaped digital collaboration and knowledge management. Originally conceptualized as a no-code toolbuilder, the platform has evolved into an ubiquitous "all-in-one" workspace utilized by millions globally. This report synthesizes available market intelligence, technical architecture analyses, financial milestones, and corporate culture evaluations to cons
```

**Artifact 2: person-research**
```
# Deep Research Report: Strategic Profile of Akshay Kothari and Cosysense Alignment Strategy

**Key Points:**
*   Research suggests Akshay Kothari, Co-Founder and Chief Operating Officer (COO) of Notion, is a central figure in the company's hyper-growth, having scaled the organization from a small startup to a global enterprise valued at an estimated $11 billion.
*   Evidence leans toward Kothari possessing a highly interdisciplinary background, bridging deep technical hardware engineering (Electrical Engineering at Purdue and Stanford) with scalable software operations and global team management.
*   It seems likely that Kothari’s operational mandate—which has historically included building out Notion’s finance, people, and infrastructure functions—makes him a critical stakeholder in the company's current real estate expansion and subsequent operational expenditures (OPEX).
*   Given Notion's recent massive physical footprint expansion (a 114,646-square-foot headquarters lease in San Francisco), Kothari is likely evaluating scalable, secure, and employee-centric facility optimization strategies as the company prepares for a potential IPO.
*   Strategic alignment between Notion and Cosysense appears exceptionally strong; Cosysense’s air-gapped LoRaWAN technology directly bypasses Notion's stringent IT security bottlenecks, while its human-centric thermal optimization perfectly aligns with Kothari's publicly stated focus on employee retention, "Craft," and Diversity, Equity, a
```

**Artifact 3: cold-email**
```
Subject: 685 Market St / HVAC & Employee Comfort

Hi there,

Congrats on the massive 114,600 sq ft lease expansion at the Monadnock Building.

As you build out the new San Francisco HQ, optimizing workplace comfort for your hybrid teams while managing Scope 2 emissions is a huge undertaking. Cosysense reduces commercial HVAC energy costs by up to 40% using AI-driven sensors that operate on an isolated private network, completely bypassing your secure IT infrastructure.

Would you be open to a brief chat about optimizing the new space at zero upfront cost?

Best,
Sebastian Horstmann
```

  [2] PASS B2B Status: {"jobId": "92", "generationId": "c1555b4b-8612-42b4-b0a2-38aa092516ed", "sessionId": "0f0757c5-6dd8-417d-ac0d-597c91ca916e", "agentType": "b2b-sales", "status": "completed", "progress": 100, "currentStep": "", "failedReason": null, "interactionData": null, "logs": null, "artifacts": [{"payload": {"c
```
{
  "jobId": "92",
  "generationId": "c1555b4b-8612-42b4-b0a2-38aa092516ed",
  "sessionId": "0f0757c5-6dd8-417d-ac0d-597c91ca916e",
  "agentType": "b2b-sales",
  "status": "completed",
  "progress": 100,
  "currentStep": "",
  "failedReason": null,
  "interactionData": null,
  "logs": null,
  "artifacts": [
    {
      "payload": {
        "content": "# Deep Research Report: Strategic Analysis of Notion Labs, Inc. and Alignment Opportunities for Cosysense\n\n**Key Points:**\n*   Research suggests Notion is a dominant force in the productivity software market, transitioning from a workspace tool to a comprehensive AI agent platform.\n*   The company's estimated annual recurring revenue (ARR) appears to have reached approximately $600 million by late 2025, largely driven by AI-enabled customers.\n*   Evidence leans toward a current valuation of $11 billion, recently solidified by a $270 million secondary tender offer in early 2026.\n*   Notion's physical footprint is expanding significantly; records indicate a recent 114,646-square-foot headquarters lease in San Francisco, presenting a substantial facility management profile.\n*   It seems likely that as Notion prepares for a potential IPO, operational efficiency and Environmental, Social, and Governance (ESG) compliance will become increasingly critical priorities.\n\n**Introduction**\nThe following comprehensive analysis examines Notion Labs, Inc. (operating as Notion), a pioneering software-as-a-service (SaaS) enterprise that has reshaped digital collaboration and knowledge management. Originally conceptualized as a no-code toolbuilder, the platform has evolved into an ubiquitous \"all-in-one\" workspace utilized by millions globally. This report synthesizes available market intelligence, technical architecture analyses, financial milestones, and corporate culture evaluations to construct a holistic profile of the organization. \n\n**Strategic Context**\nFor an academic and strategic audience, particularly those ev
```

  [3] PASS B2B Hydrate: {"session": {"id": "0f0757c5-6dd8-417d-ac0d-597c91ca916e", "userId": "4d05c369-c48e-4e01-871c-718ec19c0869", "status": "completed", "createdAt": "2026-03-23T20:52:02.957Z", "updatedAt": "2026-03-23T21:00:03.308Z", "metadata": {"agentType": "b2b-sales", "source": "api-key", "companyName": "Notion", "
```
{
  "session": {
    "id": "0f0757c5-6dd8-417d-ac0d-597c91ca916e",
    "userId": "4d05c369-c48e-4e01-871c-718ec19c0869",
    "status": "completed",
    "createdAt": "2026-03-23T20:52:02.957Z",
    "updatedAt": "2026-03-23T21:00:03.308Z",
    "metadata": {
      "agentType": "b2b-sales",
      "source": "api-key",
      "companyName": "Notion",
      "companyWebsite": "https://notion.so",
      "coldEmailGenerations": [
        {
          "generationId": "c1555b4b-8612-42b4-b0a2-38aa092516ed",
          "subject": "685 Market St / HVAC & Employee Comfort",
          "body": "Hi there,\n\nCongrats on the massive 114,600 sq ft lease expansion at the Monadnock Building.\n\nAs you build out the new San Francisco HQ, optimizing workplace comfort for your hybrid teams while managing Scope 2 emissions is a huge undertaking. Cosysense reduces commercial HVAC energy costs by up to 40% using AI-driven sensors that operate on an isolated private network, completely bypassing your secure IT infrastructure.\n\nWould you be open to a brief chat about optimizing the new space at zero upfront cost?\n\nBest,\nSebastian Horstmann",
          "toAddress": "",
          "ccAddress": "mmcginley@makenotion.com",
          "ccName": "Michael McGinley",
          "ccTitle": "Environment",
          "content": "Subject: 685 Market St / HVAC & Employee Comfort\n\nHi there,\n\nCongrats on the massive 114,600 sq ft lease expansion at the Monadnock Building.\n\nAs you build out the new San Francisco HQ, optimizing workplace comfort for your hybrid teams while managing Scope 2 emissions is a huge undertaking. Cosysense reduces commercial HVAC energy costs by up to 40% using AI-driven sensors that operate on an isolated private network, completely bypassing your secure IT infrastructure.\n\nWould you be open to a brief chat about optimizing the new space at zero upfront cost?\n\nBest,\nSebastian Horstmann",
          "storageKey": "users/4d05c369-c48e-4e01-871c-718ec19c0869/sessions/0f0757c5-6dd8
```

  Artifacts: 3, GenLogs: 1, ColdEmailVersions: 1
  [4] PASS B2B Download (company-research): {'content': '# Deep Research Report: Strategic Analysis of Notion Labs, Inc. and Alignment Opportunities for Cosysense\n\n**Key Points:**\n*   Research suggests Notion is a dominant force in the productivity software market, transitioning from a workspace tool to a comprehensive AI agent platform.\n
```
{
  "content": "# Deep Research Report: Strategic Analysis of Notion Labs, Inc. and Alignment Opportunities for Cosysense\n\n**Key Points:**\n*   Research suggests Notion is a dominant force in the productivity software market, transitioning from a workspace tool to a comprehensive AI agent platform.\n*   The company's estimated annual recurring revenue (ARR) appears to have reached approximately $600 million by late 2025, largely driven by AI-enabled customers.\n*   Evidence leans toward a current valuation of $11 billion, recently solidified by a $270 million secondary tender offer in early 2026.\n*   Notion's physical footprint is expanding significantly; records indicate a recent 114,646-square-foot headquarters lease in San Francisco, presenting a substantial facility management profile.\n*   It seems likely that as Notion prepares for a potential IPO, operational efficiency and Environmental, Social, and Governance (ESG) compliance will become increasingly critical priorities.\n\n**Introduction**\nThe following comprehensive analysis examines Notion Labs, Inc. (operating as Notion), a pioneering software-as-a-service (SaaS) enterprise that has reshaped digital collaboration and knowledge management. Originally conceptualized as a no-code toolbuilder, the platform has evolved into an ubiquitous \"all-in-one\" workspace utilized by millions globally. This report synthesizes available market intelligence, technical architecture analyses, financial milestones, and corporate culture evaluations to construct a holistic profile of the organization. \n\n**Strategic Context**\nFor an academic and strategic audience, particularly those evaluating B2B integration and vendor alignment, understanding Notion's rapid scaling vectors is paramount. The company is currently navigating the complex transition from a high-growth startup to a mature, pre-IPO enterprise. This transition is marked by explosive data infrastructure demands, a aggressive pivot toward autonomous Artifici
```

    Downloaded: 2 bytes/chars
  [5] PASS B2B Download (person-research): {'content': '# Deep Research Report: Strategic Profile of Akshay Kothari and Cosysense Alignment Strategy\n\n**Key Points:**\n*   Research suggests Akshay Kothari, Co-Founder and Chief Operating Officer (COO) of Notion, is a central figure in the company\'s hyper-growth, having scaled the organizati
```
{
  "content": "# Deep Research Report: Strategic Profile of Akshay Kothari and Cosysense Alignment Strategy\n\n**Key Points:**\n*   Research suggests Akshay Kothari, Co-Founder and Chief Operating Officer (COO) of Notion, is a central figure in the company's hyper-growth, having scaled the organization from a small startup to a global enterprise valued at an estimated $11 billion.\n*   Evidence leans toward Kothari possessing a highly interdisciplinary background, bridging deep technical hardware engineering (Electrical Engineering at Purdue and Stanford) with scalable software operations and global team management.\n*   It seems likely that Kothari\u2019s operational mandate\u2014which has historically included building out Notion\u2019s finance, people, and infrastructure functions\u2014makes him a critical stakeholder in the company's current real estate expansion and subsequent operational expenditures (OPEX).\n*   Given Notion's recent massive physical footprint expansion (a 114,646-square-foot headquarters lease in San Francisco), Kothari is likely evaluating scalable, secure, and employee-centric facility optimization strategies as the company prepares for a potential IPO.\n*   Strategic alignment between Notion and Cosysense appears exceptionally strong; Cosysense\u2019s air-gapped LoRaWAN technology directly bypasses Notion's stringent IT security bottlenecks, while its human-centric thermal optimization perfectly aligns with Kothari's publicly stated focus on employee retention, \"Craft,\" and Diversity, Equity, and Inclusion (DEI).\n\n**Introduction**\nThe following comprehensive deep research report provides a strategic, academic analysis of Akshay Kothari, Co-Founder and Chief Operating Officer of Notion Labs, Inc. This document synthesizes verified intelligence regarding his professional trajectory, operational philosophy, public thought leadership, and current responsibilities. Designed for a strategic B2B audience\u2014specifically the executive tea
```

    Downloaded: 2 bytes/chars
  [6] PASS B2B Download (cold-email): {'content': 'Subject: 685 Market St / HVAC & Employee Comfort\n\nHi there,\n\nCongrats on the massive 114,600 sq ft lease expansion at the Monadnock Building.\n\nAs you build out the new San Francisco HQ, optimizing workplace comfort for your hybrid teams while managing Scope 2 emissions is a huge u
```
{
  "content": "Subject: 685 Market St / HVAC & Employee Comfort\n\nHi there,\n\nCongrats on the massive 114,600 sq ft lease expansion at the Monadnock Building.\n\nAs you build out the new San Francisco HQ, optimizing workplace comfort for your hybrid teams while managing Scope 2 emissions is a huge undertaking. Cosysense reduces commercial HVAC energy costs by up to 40% using AI-driven sensors that operate on an isolated private network, completely bypassing your secure IT infrastructure.\n\nWould you be open to a brief chat about optimizing the new space at zero upfront cost?\n\nBest,\nSebastian Horstmann",
  "mimeType": "text/markdown"
}
```

    Downloaded: 2 bytes/chars

## Shares

  [7] FAIL Create share: [NOT_FOUND] ATS generation 'c1555b4b-8612-42b4-b0a2-38aa092516ed' not found in session
  Cleaned up session 0f0757c5-6dd8-417d-ac0d-597c91ca916e

## Resume Upload + Parse

  [8] PASS Upload resume (file): {"ok": true, "normalized": {"basics": {"name": "EBENEZER ISAAC", "label": "Senior Software Engineer | Python, TypeScript, React", "email": "ebnezr.isaac@gmail.com", "phone": "+44 75010 53232", "location": {"city": "London", "countryCode": "UK"}}, "work": [{"name": "IBM", "position": "Application Dev
```
{
  "ok": true,
  "normalized": {
    "basics": {
      "name": "EBENEZER ISAAC",
      "label": "Senior Software Engineer | Python, TypeScript, React",
      "email": "ebnezr.isaac@gmail.com",
      "phone": "+44 75010 53232",
      "location": {
        "city": "London",
        "countryCode": "UK"
      }
    },
    "work": [
      {
        "name": "IBM",
        "position": "Application Developer",
        "startDate": "2023",
        "endDate": "2025",
        "highlights": [
          "Developed static analysis tools reducing bug triage time by 70%",
          "Built Python automation preventing P1 incidents"
        ]
      },
      {
        "name": "Jatpoint",
        "position": "Full Stack Developer",
        "startDate": "2025",
        "endDate": "2026",
        "highlights": [
          "Led Phase 2 platform overhaul on AWS",
          "Engineered real-time radar chart visualization"
        ]
      }
    ],
    "education": [
      {
        "institution": "UCL",
        "area": "Systems Engineering for IoT",
        "studyType": "MSc",
        "startDate": "2025",
        "endDate": "2026"
      },
      {
        "institution": "VTU",
        "area": "Computer Science",
        "studyType": "BEng",
        "startDate": "2019",
        "endDate": "2023"
      }
    ],
    "skills": [
      {
        "name": "Technologies",
        "keywords": [
          "Python",
          "TypeScript",
          "React",
          "Node.js",
          "AWS",
          "Docker",
          "MongoDB",
          "PostgreSQL"
        ]
      }
    ]
  },
  "fileSize": 618,
  "metadata": {
    "extractionMethod": "text",
    "passes": 1,
    "confidence": {
      "overall": 0.97,
      "extraction": 0.9,
      "validation": 1
    },
    "usage": {
      "promptTokens": 665,
      "candidatesTokens": 1275,
      "totalTokens": 1940
    },
    "model": "gemini-3-flash-preview"
  }
}
```

  [9] PASS Parse resume (file): {"resume": {"basics": {"name": "EBENEZER ISAAC", "label": "Senior Software Engineer | Python, TypeScript, React", "email": "ebnezr.isaac@gmail.com", "phone": "+44 75010 53232", "location": {"city": "London", "countryCode": "UK"}}, "work": [{"name": "IBM", "position": "Application Developer", "startD
```
{
  "resume": {
    "basics": {
      "name": "EBENEZER ISAAC",
      "label": "Senior Software Engineer | Python, TypeScript, React",
      "email": "ebnezr.isaac@gmail.com",
      "phone": "+44 75010 53232",
      "location": {
        "city": "London",
        "countryCode": "UK"
      }
    },
    "work": [
      {
        "name": "IBM",
        "position": "Application Developer",
        "startDate": "2023",
        "endDate": "2025",
        "highlights": [
          "Developed static analysis tools reducing bug triage time by 70%",
          "Built Python automation preventing P1 incidents"
        ]
      },
      {
        "name": "Jatpoint",
        "position": "Full Stack Developer",
        "startDate": "2025",
        "endDate": "2026",
        "highlights": [
          "Led Phase 2 platform overhaul on AWS",
          "Engineered real-time radar chart visualization"
        ]
      }
    ],
    "education": [
      {
        "institution": "UCL",
        "area": "Systems Engineering for IoT",
        "studyType": "MSc",
        "startDate": "2025",
        "endDate": "2026"
      },
      {
        "institution": "VTU",
        "area": "Computer Science",
        "studyType": "BEng",
        "startDate": "2019",
        "endDate": "2023"
      }
    ],
    "skills": [
      {
        "name": "Software Development",
        "keywords": [
          "Python",
          "TypeScript",
          "React",
          "Node.js",
          "AWS",
          "Docker",
          "MongoDB",
          "PostgreSQL"
        ]
      }
    ]
  },
  "metadata": {
    "confidence": {
      "overall": 0.97,
      "extraction": 0.9,
      "validation": 1
    },
    "detectedLanguage": "en",
    "detectedFormat": "standard",
    "pageCount": 1,
    "warnings": [
      "Summary is empty (most themes show it prominently)"
    ],
    "extractionMethod": "text",
    "passes": 1,
    "usage": {
      "promptTokens": 665,
      "candidatesTokens": 1893,
      "totalTokens": 2558
  
```


## Resume Validate + Render + Preview

  [10] PASS Validate resume: {"valid": true, "errors": [], "warnings": [{"path": "basics.phone", "message": "Phone is missing (some recruiters prefer phone calls)"}], "coerced": {"basics": {"name": "Test User", "label": "Software Engineer", "email": "test@example.com", "summary": "Experienced engineer", "location": {"city": "Lo
```
{
  "valid": true,
  "errors": [],
  "warnings": [
    {
      "path": "basics.phone",
      "message": "Phone is missing (some recruiters prefer phone calls)"
    }
  ],
  "coerced": {
    "basics": {
      "name": "Test User",
      "label": "Software Engineer",
      "email": "test@example.com",
      "summary": "Experienced engineer",
      "location": {
        "city": "London",
        "countryCode": "UK"
      },
      "profiles": []
    },
    "work": [
      {
        "name": "Acme Corp",
        "position": "Engineer",
        "startDate": "2020-01-01",
        "summary": "Built things",
        "highlights": [
          "Led team of 5"
        ]
      }
    ],
    "education": [
      {
        "institution": "MIT",
        "area": "Computer Science",
        "studyType": "BS",
        "startDate": "2016-01-01",
        "endDate": "2020-01-01"
      }
    ],
    "skills": [
      {
        "name": "Python",
        "keywords": [
          "Django",
          "FastAPI"
        ]
      }
    ]
  }
}
```

  [11] PASS Render resume (PDF): {"pdf": "JVBERi0xLjQKJdPr6eEKMSAwIG9iago8PC9DcmVhdG9yIChDaHJvbWl1bSkKL1Byb2R1Y2VyIChTa2lhL1BERiBtMTIwKQovQ3JlYXRpb25EYXRlIChEOjIwMjYwMzIzMjAzNjE4KzAwJzAwJykKL01vZERhdGUgKEQ6MjAyNjAzMjMyMDM2MTgrMDAnMDAnKT4+CmVuZG9iagozIDAgb2JqCjw8L2NhIDEKL0JNIC9Ob3JtYWw+PgplbmRvYmoKNSAwIG9iago8PC9DQSAxCi9jYSAxCi9MQyA
```
{
  "pdf": "JVBERi0xLjQKJdPr6eEKMSAwIG9iago8PC9DcmVhdG9yIChDaHJvbWl1bSkKL1Byb2R1Y2VyIChTa2lhL1BERiBtMTIwKQovQ3JlYXRpb25EYXRlIChEOjIwMjYwMzIzMjAzNjE4KzAwJzAwJykKL01vZERhdGUgKEQ6MjAyNjAzMjMyMDM2MTgrMDAnMDAnKT4+CmVuZG9iagozIDAgb2JqCjw8L2NhIDEKL0JNIC9Ob3JtYWw+PgplbmRvYmoKNSAwIG9iago8PC9DQSAxCi9jYSAxCi9MQyAxCi9MSiAxCi9MVyAyCi9NTCA0Ci9TQSB0cnVlCi9CTSAvTm9ybWFsPj4KZW5kb2JqCjcgMCBvYmoKPDwvVHlwZSAvQW5ub3QKL1N1YnR5cGUgL0xpbmsKL0YgNAovQm9yZGVyIFswIDAgMF0KL1JlY3QgWzIxNi4wMDAwMiA2NjIuNjY5OTggMjg0LjI1MDAzIDY3Mi40MTk5OF0KL0EgPDwvVHlwZSAvQWN0aW9uCi9TIC9VUkkKL1VSSSAobWFpbHRvOnRlc3RAZXhhbXBsZS5jb20pPj4KL1N0cnVjdFBhcmVudCAxMDAwMDA+PgplbmRvYmoKOCAwIG9iago8PC9GaWx0ZXIgL0ZsYXRlRGVjb2RlCi9MZW5ndGggMzI4Mj4+IHN0cmVhbQp4nM1bW8seN5K+71+h64GV66iqghCIHSfMRWAyY5gf8O0my2IvJHs1/34otbpb/Z6+g8OSOMT9VrekOj5VKimVOPo/BQqU/6jTTxesgRFenr4svy3IVhUAUAsi9UfwQgRckZQKk/n69Pt/Lf/8S/nf5belvwIA6rMfv27P9fRlwZJ//v5jWR9+/3V59yOXX/9vyfEGWhAkcoFflhpKUWpoy/828Bx2Tfz9130sNRpDIbxURGulIhv3kZe0339d3n9a3v2tfPPNu58+/PX7AuXbb99//2F594MUbOXTLwuuSsNCJMWofPqyfAPA9m359D+LVdNwNytQPv1n+QZAvL/wys4eGvsLbf1FqyEc4McIXafSGs2C2k4H7nSu4BatHTPxugRibRauys+vcZ8r7S8+/vRh+fhpqUKspUprVqqCRlfaFfFKazhrja+05rZpbePPPf1PDjZoqJPIAQkPxqO/kMoOEe1Ka1JdfHXlQf+u06OGOoD5MZOMtTUQgOVSBVqJPcLlUmmtOhIg2qVl0qcDgI4X5EMMVQaYmMJ74n03lmjCADqt/WEYn8kB6CVT3eP27osL278pXmi2PF5ZHhmH6WnjggNz1p2J90P7KgI+ub/yGABG4KSX8mi1JuB85ctShRk07FKZVB0bXNn3xkQ4lkZs4H68kDZGIBu0uNLx9VRi21QSEHwV3VSRGBjb13D13RjRCMFcn5P7/kR3pXhG5cOFfl5+Xn5bfOB+K42wuim0opD/HjmDKjgzs3ZnOX7dGvv05cW++e5HzTxCWBDKl/63FaRCXP61rH9zkjjfPyW0AhCwl6gCgellXEEdSFrx6iSgnjQ0lpZIVkmkkffB5B4AUqy2phgtClfRMPZiFYHU3QrX5hqmrbSq2hyY+uBAIiQvrQIioHGRih4K0opWCVJuWqQqmitK0QqA3CDKUwe9huHY3wO6eNFKGBScNFA1saK1sWFOw7Wxg1gObhVUwsIL10zs4smEQqioF6ouJghRLJXjLFGoKgYxW3laLFnDVA9VDARtWrwCggFSyVqCQ9KQKaw25YK1uXmIlqclUi1CLgWrNHRRKZHag2j5JQUSEFhBSEVrZj2saBpNSMrTgtCNwq0VrNDAqCXurNaDTgRGMM2ao44qZyI+LVmJBDg23enCBXldBXSflzyppircJVu5wLQeSmWWAPSNZwwtKNXT0G67dDmHVhEWzsehCc4ptIYHRdt1xgXTDObGuiu3EyMCG+9m6FKkHUCUdoNZQashChi7YVtBr9zIG+0ukEZEr+Zg0A5fwaio7HC4
```

  [12] PASS Preview resume (HTML): {"html": "<!doctype html>\n    <html lang=\"en\" style=\"\">\n      <head>\n<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n<link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=S
```
{
  "html": "<!doctype html>\n    <html lang=\"en\" style=\"\">\n      <head>\n<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n<link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&display=swap\" rel=\"stylesheet\">\n        <meta charset=\"utf-8\" />\n        \n    <title>Test User</title>\n    <meta name=\"description\" content=\"Experienced engineer\" />\n  \n        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n        <link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css?family=Lato:400,700&display=swap\" />\n        <style>\n          :root{color-scheme:light dark;--color-background-light: #ffffff;--color-dimmed-light: #f3f4f5;--color-primary-light: #191e23;--color-secondary-light: #6c7781;--color-accent-light: #0073aa;--color-background-dark: #191e23;--color-dimmed-dark: #23282d;--color-primary-dark: #fbfbfc;--color-secondary-dark: #ccd0d4;--color-accent-dark: #00a0d2;--color-background: var(--color-background-light);--color-dimmed: var(--color-dimmed-light);--color-primary: var(--color-primary-light);--color-secondary: var(--color-secondary-light);--color-accent: var(--color-accent-light);--scale-ratio: 1.25;--scale0: 1rem;--scale1: calc(var(--scale0) * var(--scale-ratio));--scale2: calc(var(--scale1) * var(--scale-ratio));--scale3: calc(var(--scale2) * var(--scale-ratio));--scale4: calc(var(--scale3) * var(--scale-ratio));--scale5: calc(var(--scale4) * var(--scale-ratio))}@media (prefers-color-scheme: dark){:root{--color-background: var(--color-background-dark);--color-dimmed: var(--color-dimmed-dark);--color-primary: var(--color-primary-dark);--color-secondary: var(--color-secondary-dark);--color-accent: var(--color-accent-dark)}}*{box-sizing:border-box;margin:0;padding:0}html{font-size:14px}body{background:var(--color-b
```


## Master Resume CRUD

  [13] PASS Create master resume: {"id": "3b3f893b-df3f-46ec-8b33-18504107dc6f", "label": "SDK E2E Test Resume", "rawText": "EBENEZER ISAAC\nSenior Software Engineer | Python, TypeScript, React\nLondon, UK | ebnezr.isaac@gmail.com | +44 75010 53232\n\nEXPERIENCE:\nApplication Developer, IBM (2023-2025)\n- Developed static analysis t
```
{
  "id": "3b3f893b-df3f-46ec-8b33-18504107dc6f",
  "label": "SDK E2E Test Resume",
  "rawText": "EBENEZER ISAAC\nSenior Software Engineer | Python, TypeScript, React\nLondon, UK | ebnezr.isaac@gmail.com | +44 75010 53232\n\nEXPERIENCE:\nApplication Developer, IBM (2023-2025)\n- Developed static analysis tools reducing bug triage time by 70%\n- Built Python automation preventing P1 incidents\n\nFull Stack Developer, Jatpoint (2025-2026)\n- Led Phase 2 platform overhaul on AWS\n- Engineered real-time radar chart visualization\n\nEDUCATION:\nMSc Systems Engineering for IoT, UCL (2025-2026)\nBEng Computer Science, VTU (2019-2023)\n\nSKILLS: Python, TypeScript, React, Node.js, AWS, Docker, MongoDB, PostgreSQL\n",
  "structured": null,
  "isDefault": false,
  "createdAt": "2026-03-23T21:00:26.116Z",
  "updatedAt": "2026-03-23T21:00:26.116Z"
}
```

  [14] PASS List masters: {"resumes": [{"id": "3b3f893b-df3f-46ec-8b33-18504107dc6f", "label": "SDK E2E Test Resume", "rawText": "EBENEZER ISAAC\nSenior Software Engineer | Python, TypeScript, React\nLondon, UK | ebnezr.isaac@gmail.com | +44 75010 53232\n\nEXPERIENCE:\nApplication Developer, IBM (2023-2025)\n- Developed stat
```
{
  "resumes": [
    {
      "id": "3b3f893b-df3f-46ec-8b33-18504107dc6f",
      "label": "SDK E2E Test Resume",
      "rawText": "EBENEZER ISAAC\nSenior Software Engineer | Python, TypeScript, React\nLondon, UK | ebnezr.isaac@gmail.com | +44 75010 53232\n\nEXPERIENCE:\nApplication Developer, IBM (2023-2025)\n- Developed static analysis tools reducing bug triage time by 70%\n- Built Python automation preventing P1 incidents\n\nFull Stack Developer, Jatpoint (2025-2026)\n- Led Phase 2 platform overhaul on AWS\n- Engineered real-time radar chart visualization\n\nEDUCATION:\nMSc Systems Engineering for IoT, UCL (2025-2026)\nBEng Computer Science, VTU (2019-2023)\n\nSKILLS: Python, TypeScript, React, Node.js, AWS, Docker, MongoDB, PostgreSQL\n",
      "structured": null,
      "isDefault": false,
      "createdAt": "2026-03-23T21:00:26.116Z",
      "updatedAt": "2026-03-23T21:00:26.116Z"
    }
  ],
  "total": 1
}
```

  [15] PASS Get master: {"id": "3b3f893b-df3f-46ec-8b33-18504107dc6f", "label": "SDK E2E Test Resume", "rawText": "EBENEZER ISAAC\nSenior Software Engineer | Python, TypeScript, React\nLondon, UK | ebnezr.isaac@gmail.com | +44 75010 53232\n\nEXPERIENCE:\nApplication Developer, IBM (2023-2025)\n- Developed static analysis t
```
{
  "id": "3b3f893b-df3f-46ec-8b33-18504107dc6f",
  "label": "SDK E2E Test Resume",
  "rawText": "EBENEZER ISAAC\nSenior Software Engineer | Python, TypeScript, React\nLondon, UK | ebnezr.isaac@gmail.com | +44 75010 53232\n\nEXPERIENCE:\nApplication Developer, IBM (2023-2025)\n- Developed static analysis tools reducing bug triage time by 70%\n- Built Python automation preventing P1 incidents\n\nFull Stack Developer, Jatpoint (2025-2026)\n- Led Phase 2 platform overhaul on AWS\n- Engineered real-time radar chart visualization\n\nEDUCATION:\nMSc Systems Engineering for IoT, UCL (2025-2026)\nBEng Computer Science, VTU (2019-2023)\n\nSKILLS: Python, TypeScript, React, Node.js, AWS, Docker, MongoDB, PostgreSQL\n",
  "structured": null,
  "isDefault": false,
  "createdAt": "2026-03-23T21:00:26.116Z",
  "updatedAt": "2026-03-23T21:00:26.116Z"
}
```

  [16] PASS Update master: {"id": "3b3f893b-df3f-46ec-8b33-18504107dc6f", "label": "Updated Label", "rawText": "EBENEZER ISAAC\nSenior Software Engineer | Python, TypeScript, React\nLondon, UK | ebnezr.isaac@gmail.com | +44 75010 53232\n\nEXPERIENCE:\nApplication Developer, IBM (2023-2025)\n- Developed static analysis tools r
```
{
  "id": "3b3f893b-df3f-46ec-8b33-18504107dc6f",
  "label": "Updated Label",
  "rawText": "EBENEZER ISAAC\nSenior Software Engineer | Python, TypeScript, React\nLondon, UK | ebnezr.isaac@gmail.com | +44 75010 53232\n\nEXPERIENCE:\nApplication Developer, IBM (2023-2025)\n- Developed static analysis tools reducing bug triage time by 70%\n- Built Python automation preventing P1 incidents\n\nFull Stack Developer, Jatpoint (2025-2026)\n- Led Phase 2 platform overhaul on AWS\n- Engineered real-time radar chart visualization\n\nEDUCATION:\nMSc Systems Engineering for IoT, UCL (2025-2026)\nBEng Computer Science, VTU (2019-2023)\n\nSKILLS: Python, TypeScript, React, Node.js, AWS, Docker, MongoDB, PostgreSQL\n",
  "structured": null,
  "isDefault": false,
  "createdAt": "2026-03-23T21:00:26.116Z",
  "updatedAt": "2026-03-23T21:00:27.036Z"
}
```

  [17] PASS Delete master: 204 No Content


## Content Save

  [18] PASS Save content (original_cv): {'success': True}
```
{
  "success": true
}
```


============================================================
  TOTAL: 18 PASS / 1 FAIL (19 tests)
============================================================