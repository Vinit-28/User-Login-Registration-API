

This is an internship assignment given by SIRPI Products & Services Private Limited.

Technologies Used :
1. Python-Flask
2. MongoDB


Let's discuss how to use it :

1. To Login

    Make a GET request to url "https://sirpi-app.herokuapp.com/login" with the following parameters :
    {
        username : "Your Username",
        password : "Your Password"
    }


2. To Register

    Make a POST request to url "https://sirpi-app.herokuapp.com/regitser" with the following parameters :
    {
        username : "Your Username",
        password : "Your Password"
        name : "Your Name",
        description : "Any Description Part",
        mobile : "Contact Number"
    }


3. To get All Registered Users Info

    Make a GET request to url "https://sirpi-app.herokuapp.com/all_users".


4. To Logout

    Make a GET request to url "https://sirpi-app.herokuapp.com/logout" with the following parameters :
    {
        username : "Your Username"
    }


5. To Reset Your Password

    Make a PUT request to url "https://sirpi-app.herokuapp.com/reset_password" with the following parameters :
    {
        username : "Your Username",
        old_password : "Your Old Password",
        new_password : "Your New Password"
    }