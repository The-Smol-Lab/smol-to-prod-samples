# 🛡️ Using Auth0 Authentication with AWS Bedrock AgentCore

## Overview

Auth0 can be used as a **free authentication provider** for AWS Bedrock AgentCore. It is one of the **built-in identity providers (IdPs)** supported by AgentCore.

**Docs:**

* [AWS Identity Providers – Auth0](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-idp-auth0.html)
* [Bedrock AgentCore Developer Guide (PDF)](https://docs.aws.amazon.com/pdfs/bedrock-agentcore/latest/devguide/bedrock-agentcore-dg.pdf)
* [Perplexity: Set up Auth0 for AgentCore Runtime](https://www.perplexity.ai/search/set-up-auth0-for-agentcore-run-JmiZwDXCQEeYyPjJ4tpjPw#2)

---

## Authentication Types

| Type                        | Purpose                                                           |
| --------------------------- | ----------------------------------------------------------------- |
| **Inbound Authentication**  | Verifies incoming requests to your runtime using JWT/OIDC tokens. |
| **Outbound Authentication** | Allows your agent to securely call external APIs.                 |

---

## Runtime Invocation Pattern

```
https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{encoded-agent-arn}/invocations?qualifier={ENDPOINT_NAME}
```

**Example (redacted):**

```bash
region="ap-southeast-1"
encoded-agent-arn="arn:aws:bedrock-agentcore:ap-southeast-1:ACCOUNT_ID:runtime/your-agent-runtime-id"
ENDPOINT_NAME="DEFAULT"
```

---

## Auth0 Discovery URL Pattern

Auth0 provides an **OpenID Connect Discovery Endpoint** used by AWS AgentCore for identity validation.

**Pattern:**

```
https://{tenant-region}.auth0.com/.well-known/openid-configuration
```

Here, `{tenant-region}` usually combines both your **tenant name** and **Auth0 region domain**. For example:

* For tenants in the US region: `https://myapp.us.auth0.com/.well-known/openid-configuration`
* For tenants in Japan region: `https://myapp.jp.auth0.com/.well-known/openid-configuration`

**Example (safe version):**

```
https://example-tenant.jp.auth0.com/.well-known/openid-configuration
```

### Key Fields from Discovery Document

| Field                                   | Purpose                                               |
| --------------------------------------- | ----------------------------------------------------- |
| `issuer`                                | Identifies your Auth0 tenant’s OIDC issuer URL        |
| `authorization_endpoint`                | Used during OAuth2 authorization code flow            |
| `token_endpoint`                        | Issues and refreshes access tokens                    |
| `jwks_uri`                              | Public key location for JWT signature verification    |
| `userinfo_endpoint`                     | Retrieves authenticated user info                     |
| `end_session_endpoint`                  | Used for logout support                               |
| `scopes_supported`                      | Available scopes (`openid`, `profile`, `email`, etc.) |
| `response_types_supported`              | Valid OAuth2 response types                           |
| `code_challenge_methods_supported`      | PKCE methods (`S256`, `plain`)                        |
| `id_token_signing_alg_values_supported` | Supported signing algorithms (e.g., `RS256`, `PS256`) |

---

## How It Works (Simplified Flow)

1. Configure Auth0 as an **OIDC provider** in AgentCore Identity settings.
2. Retrieve the **Discovery URL** and **JWKS URI** from Auth0.
3. Use Auth0 to issue JWT/OAuth2 access tokens via its `token_endpoint`.
4. When invoking the AgentCore runtime endpoint, include:

   ```bash
   Authorization: Bearer <ACCESS_TOKEN>
   ```
5. AgentCore verifies the JWT signature and claims using the discovery metadata.

---

## Example Runtime Invocation

```js
const endpoint = "https://bedrock-agentcore.ap-southeast-1.amazonaws.com/runtimes/<encoded-agent-arn>/invocations?qualifier=DEFAULT";

const response = await fetch(endpoint, {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${accessToken}`, // from Auth0 OAuth2 flow
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ prompt: "Hello AgentCore!" })
});
```

---

## Security Notes

* Do **not** expose Auth0 tenant domain, client ID, or Agent ARN publicly.
* Store secrets securely in **AWS SSM Parameter Store** or **AWS Secrets Manager**.
* Ensure `aud` (audience) and `iss` (issuer) claims match AgentCore runtime expectations.
* Prefer **RS256** or stronger signing algorithms for token security.

---

## References

* [AWS Bedrock AgentCore Auth0 Guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-idp-auth0.html)
* [Auth0 OpenID Connect Documentation](https://auth0.com/docs/protocols/protocol-oauth2)
* [OIDC Discovery Specification](https://openid.net/specs/openid-connect-discovery-1_0.html)
* [Auth0 - Getting Started](https://manage.auth0.com/dashboard/jp/smol-lab/)
