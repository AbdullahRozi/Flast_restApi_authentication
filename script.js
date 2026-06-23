
        // 1. Corrected the spelling from "RegiaterForm" to "RegisterForm"
                localStorage.removeItem("myToken");
                const Reg_formData = document.getElementById("RegisterForm");
                const errorMessage = document.getElementById("errorMessage");

                // 2. Kept your asynchronous function structure
                async function RegisterForm(event) {
                    // Corrected to standard form prevention syntax
                    event.preventDefault();
                    
                    const Reg_form_name = document.getElementById("name");
                    const Reg_form_email = document.getElementById("email");
                    // Note: Make sure to add this password input to your HTML!
                    const Reg_form_password = document.getElementById("password"); 
                    const Reg_form_C_password = document.getElementById("C_password");

                    
                    
                
                    
                    // Check if the password field actually exists before reading its value
                    const passwordValue = Reg_form_password ? Reg_form_password.value : "";
                    const C_passwordValue = Reg_form_C_password ? Reg_form_C_password.value : "";


                    if (passwordValue !== C_passwordValue) {
                        errorMessage.style.display = 'block'; 
                        return; 
                    }
                        errorMessage.style.display = 'none';

                    try {
                        const response = await fetch('http://127.0.0.1:5000/api/register', {
                            method: 'POST', 
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                name: Reg_form_name.value,
                                email: Reg_form_email.value,
                                password: passwordValue ,
                                C_password: C_passwordValue
                            })
                        });

                                // Useful for debugging your server response
                                const data = await response.json();

                                console.log("Server response:", data);
                                localStorage.setItem("myToken" , data.token)
                                FormData.value = " "

                                window.location.href = "C:/Users/pcs/Desktop/python%20projects%20practice/dashboard.html"
                                

                                
                            } catch (error) {
                                console.error("Error submitting form:", error);
                            }
                        }

                        // 3. Corrected the second argument to call the function "RegisterForm"
                        Reg_formData.addEventListener("submit", RegisterForm);

                            
                        
      // FROM HERE LOGIN DATA STARTING
      const login_form =  document.getElementById("LoginForm");
      async function LoginForm(event) {
                    // Corrected to standard form prevention syntax
                    event.preventDefault();
                    const log_form_email = document.getElementById("L_email");
                    const log_form_password = document.getElementById("L_password");
                     try {
                        const response = await fetch('http://127.0.0.1:5000/api/login', {
                            method: 'POST', 
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                email: log_form_email.value,
                                password: log_form_password.value
                            })
                        });
                            
                        if (response.ok){
                                // Useful for debugging your server response
                                const data = await response.json();

                                console.log("Server response:", data);
                                localStorage.setItem("myToken" , data.token)
                               

                                window.location.href = "C:/Users/pcs/Desktop/python%20projects%20practice/dashboard.html"
                                
                        }else{
                            const data = await response.json();
                            errorMessage.textContent = data.message ;
                            errorMessage.style.color = 'red' ;
                        }
                                
                            } catch (error) {
                                console.error("Error submitting form:", error);
                            }   }

        
        
        login_form.addEventListener("submit" , LoginForm);