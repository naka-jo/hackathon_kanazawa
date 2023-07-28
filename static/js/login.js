function inputcheck() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const submit = document.getElementById("submit");
    if (email!="" && password!=""){
        submit.disabled = false;
    }else{
        submit.disabled = true;
    }
}