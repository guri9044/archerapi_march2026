# PowerShell script to create bulk users in Archer API

$url = "https://archer-irm.com/Archer/platformapi/core/security/login"

$requestBody = @{
    InstanceName = "t202603"
    Username = "api.user"
    UserDomain = ""
    Password = "Archer@123"
} | ConvertTo-Json

$requestHeaders = @{
    "Content-Type" = "application/json"
}

$response = Invoke-RestMethod -Uri $url -Method Post -Body $requestBody -Headers $requestHeaders

$sessionToken = $response.RequestedObject.SessionToken
Write-Host $sessionToken

$url = "https://archer-irm.com/Archer/platformapi/core/system/user"

$users_data = Import-Csv -Path 'Users.csv'

$headers = @{
    "Authorization" = "Archer session-id=`"$sessionToken`""
    "Content-Type" = "application/json"
}

foreach ($user in $users_data) {
    $payload = @{
        User = @{
            UserName = $user.Username
            FirstName = $user.FirstName
            LastName = $user.LastName
        }
        Password = $user.Password
    } | ConvertTo-Json

    $response2 = Invoke-RestMethod -Uri $url -Method Post -Body $payload -Headers $headers
    $userID = $response2.RequestedObject.Id

    $groupIDs = $user.Group -split '/'
    foreach ($groupID in $groupIDs) {
        $grouppayload = @{
            UserId = $userID
            GroupId = $groupID
            IsAdd = $true
        } | ConvertTo-Json

        $groupurl = "https://archer-irm.com/Archer/platformapi/core/system/usergroup"
        $response3 = Invoke-RestMethod -Uri $groupurl -Method Put -Body $grouppayload -Headers $headers
        Write-Host $response3
    }
}