# API Documentation


> ##### Base Endpoint: https://api.farmci.com/
#
#### Available endpoints, descriptions and usage
<table cellpadding="4" cellspacing="3">
    <tr style="">
        <th>Endpoint</th>
        <th>Descriptions</th>
    </tr>
        <tr>
            <td> <a href="#login">.../accounts/login</a> </td>
             <td>
                <b>Login into a FarmCI user profile account</b>
            </td>
        </tr>
    <tr>
        <td> <a href="#register">.../db/accounts/register</a> </td>
        <td>
            <b>Register a new account into FarmCI directory</b>
        </td>
    </tr>
    <tr>
        <td><a href="#keyword-search">.../db/search?key</a></td>
         <td>
            <b>Search FarmCI farm Directory using keywords</b>
        </td>
    </tr>

</table>

##

##

### Documentation Descriptions

<h3 id="login"> Login API</h3> 

``` 
Method: POST
Login endpoint: /accounts/login
```

Logs into a FarmCI account profile: 
Get the authentication token for authorizing 
subsequent requests

<b>Request body</b>

```json
{
  "username": "GENERATED USERNAME",
  "password": "ACCOUNT PASSWORD"
}
```
<b>Success Response:  <em>status code: 200 </em> </b>
```json
{
    "success": true,
    "message": "login success",
    "token": "2589bba39f06cbc2db172c9430caf5aed40d003e"
}
```
<b>
    Failed Response: Invalid / Unregistered Credential<br>
    <em>status code: 403 </em>
</b>

```json
{
    "success": false,
    "message": "Invalid username"
}
```


#
<h3 id="register">Registration API</h3>

```
Method: POST
Login endpoint: .../db/accounts/register
```


Register a new farmer profile. 
On successful registration, a unique username will be generated for the 
registered profile
<table>
    <tr>
        <th>parameters</th>
        <th>Descriptions</th>
    </tr>
    <tr>
        <td>first_name: string</td>
        <td>First name of the farmer / User</td>
    </tr>
    <tr>
        <td>last_name: string</td>
        <td>Last name of the farmer / User</td>
    </tr>
    <tr>
        <td>password: string</td>
        <td>User's password</td>
    </tr>
    <tr>
        <td>email: string</td>
        <td>Email of the farmer / User</td>
    </tr>
    <tr>
        <td>phone: int</td>
        <td>User phone number</td>
    </tr>
    <tr>
        <td>nin (Optional): string</td>
        <td>National identity Number(NIN) of the user. It must match
            the name on the user first_name and last_name.
        </td>
    </tr>
    <tr>
        <td>bvn (Optional): string</td>
        <td>Bank verification Number(BVN).
            Name must match first_name and last_name
        </td>
    </tr>
    <tr>
        <td>gender: string</td>
        <td>male / female</td>
    </tr>
    <tr>
        <td>street_address: string</td>
        <td>User street address</td>
    </tr>
    <tr>
        <td>crop_type: string</td>
        <td>Farmer's production</td>
    </tr>
    <tr>
        <td>state: string</td>
        <td>Residential state of the user</td>
    </tr>
    <tr>
        <td>country: string</td>
        <td>Resident country</td>
    </tr>

</table>

<b>Request Body</b>
```json
{
  
  "account": {
    "first_name": "EXAMPLE FIRST NAME",
    "last_name": "EXAMPLE LAST NAME",
    "email": "example@email.com",
    "phone": "1111111111",
    "password": "myPassword"
  },
  "nin": "14262728101202",
  "bvn": "12933390303",
  "crop_type": "maize"
  "gender": "male",
  "street_address": "12, PO BOX, Angeles Avenue",
  "state": "Lagos",
  "country": "Nigeria"
}
```

<b>Success Response: <em>status code: 200</em> </b>
```json
{
  "success": true,
  "responseMessage": "success",
  "responseBody": {
    "login": {
      "username": "FSI_Generated Username",
      "password": "myPassword",
      "login_url": "https://api.farmci.com/accounts/login"
    },
    "message": "FSI_Generated Useraname has been registered",
    "info": "Proceed to login to get authentication token"
  }
}
```

<b> Failed Response. <em>status code: 400 </em>: Used credentials </b>

```json
{
  "success": false,
  "responseMessage": "email used",
  "responseBody": {
    "errors": {
      "account": {
        "email": "A user with this email already exists",
        "phone": "A user with this phone already exists"
      }
    }
  }
  
}
```


#
<h3 id="keyword-search"> Search Farm Directory </h3>

```
Method: GET
Endpoint: ../db/search/?key
```

Search our farm directory database using keywords. This search focuses
on farmers phone, number, state and crop type. The key could be a state name, 
crop type name (e.g. maize, cassava, tomatoes) or a phone number prefix.

<b> Success Response. <em>status code: 200</em> </b>

```json
{
  "success": true,
  "responseMessage": "success",
  "responseBody": {
    "no_of_matches": 5000,
    "results": [
      {
        "first_name": "Farmer 1",
        "last_name": "Last name",
        "phone": "08123850878",
        "crop_type": "maize",
        "state": "Lagos"
      },
      
      ...,
      
      {
        "first_name": "Farmer 2000",
        "last_name": "Last name",
        "phone": "09128389922",
        "crop_type": "cocoa",
        "state": "Ogun"
      }
      
    ]
    
  }
}
```

<b> No match Response: <em>status code: 404</em></b>

```json
{
  "success": true,
  "responseMessage": "no match",
  "responseBody": "no match"
}
```




#
#
> FarmCI Developers Team
