function inputcheck() {
    const email = document.getElementById("email").value;
    const password1 = document.getElementById("password").value;
    const password2 = document.getElementById("repassword").value;

    const submit = document.getElementById("submit");
    if (password1===password2 && password1!="" && password2!="" && email!=""){
        submit.disabled = false;
    }else{
        submit.disabled = true;
    }
}