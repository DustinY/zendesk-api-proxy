# Okta Auth
Once you have your user set up in Okta, you can authenticate them with MFA with or without the UI. 

## No UI Flow
The general flow would be
1. Login request
2. MFA verify

The login request will return a status of __MFA_REQURIED__. There will also be a list of factors. When the MFA verify endpoint is called, the factor id will be required to identify which MFA is being used. If MFA is not used, the MFA verify reponse example should be the same as the login response example.
The API documentation can be found [here](https://developer.okta.com/docs/reference/api/authn/)
Users can be created through the okta APIs as well.
### Login Request Example:
```
curl -v -X POST \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H "User-Agent: Mozilla/5.0 (${systemInformation}) ${platform} (${platformDetails}) ${extensions}" \
-d '{
  "username": "dade.murphy@example.com",
  "password": "correcthorsebatterystaple",
  "options": {
    "multiOptionalFactorEnroll": false,
    "warnBeforePasswordExpired": false
  }
}' "https://${yourOktaDomain}/api/v1/authn"
```
### Login Response Example with MFA:
```{
  "stateToken": "007ucIX7PATyn94hsHfOLVaXAmOBkKHWnOOLG43bsb",
  "expiresAt": "2015-11-03T10:15:57.000Z",
  "status": "MFA_REQUIRED",
  "_embedded": {
    "user": {
      "id": "00ub0oNGTSWTBKOLGLNR",
      "passwordChanged": "2015-09-08T20:14:45.000Z",
      "profile": {
        "login": "dade.murphy@example.com",
        "firstName": "Dade",
        "lastName": "Murphy",
        "locale": "en_US",
        "timeZone": "America/Los_Angeles"
      }
    },
    "factors": [
      {
        "id": "ostfm3hPNYSOIOIVTQWY",
        "factorType": "token:software:totp",
        "provider": "OKTA",
        "profile": {
          "credentialId": "dade.murphy@example.com"
        },
        "_links": {
          "verify": {
            "href": "https://{yourOktaDomain}/api/v1/authn/factors/ostfm3hPNYSOIOIVTQWY/verify",
            "hints": {
              "allow": [
                "POST"
              ]
            }
          }
        }
      },
      {
        "id": "sms193zUBEROPBNZKPPE",
        "factorType": "sms",
        "provider": "OKTA",
        "profile": {
          "phoneNumber": "+1 XXX-XXX-1337"
        },
        "_links": {
          "verify": {
            "href": "https://{yourOktaDomain}/api/v1/authn/factors/sms193zUBEROPBNZKPPE/verify",
            "hints": {
              "allow": [
                "POST"
              ]
            }
          }
        }
      },
    ]
  },
  "_links": {
    "cancel": {
      "href": "https://{yourOktaDomain}/api/v1/authn/cancel",
      "hints": {
        "allow": [
          "POST"
        ]
      }
    }
  }
}
```
### MFA Verify Request Example:
```
curl -v -X POST \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H "User-Agent: Mozilla/5.0 (${systemInformation}) ${platform} (${platformDetails}) ${extensions}" \
-d '{
  "stateToken": "007ucIX7PATyn94hsHfOLVaXAmOBkKHWnOOLG43bsb",
  "passCode": "657866"
}' "https://${yourOktaDomain}/api/v1/authn/factors/ostfm3hPNYSOIOIVTQWY/verify"
```
### MFA Verify Resposne Exampe:
```
{
  "expiresAt": "2015-11-03T10:15:57.000Z",
  "status": "SUCCESS",
  "sessionToken": "00t6IUQiVbWpMLgtmwSjMFzqykb5QcaBNtveiWlGeM",
  "_embedded": {
    "user": {
      "id": "00ub0oNGTSWTBKOLGLNR",
      "passwordChanged": "2015-09-08T20:14:45.000Z",
      "profile": {
        "login": "dade.murphy@example.com",
        "firstName": "Dade",
        "lastName": "Murphy",
        "locale": "en_US",
        "timeZone": "America/Los_Angeles"
      }
    }
  }
}
```
## UI Flow
For the UI flow, Okta provides an SDK that does a lot of the heavy lifting. You can create/design the UI from your Okta account, and then use it with the SDK. Docs for that are [here](https://developer.okta.com/docs/guides/sign-into-web-app-redirect/python/main/#require-authentication-for-everything
Essentially in you API, you would need to provide
1. an initial login endpoint (used to redirect to okta using the sdk)
2. a callback endpoint that you would need to setup okta to call. This is were okta will redirect the user after login. You could have this endpoint receive the okta token and then return the token
3. Optional: a logout endpoint to log users out

The general flow would look something like this
client goes to login endpoint/page -> page redirects user to okta login ui (sdk handles this) -> okta redirects user to callback -> callback reads token from okta and returns to user.  