import Axios from "axios";
import { useState } from "react";

const Login = () => {
    const [loginData, setLoginData] = useState({
        email: "",
        password: ""
    });

    function handleChange (e) {
        const {name, value} = e.target;

        setLoginData((prevState) => ({
        ...prevState,
        [name]: value
        }));
    }

    async function submit(e) {
        e.preventDefault();

        const data = {
            ...loginData
        };
        
        try {
            await Axios.post("/api/login", data);
        } catch (err) {
            alert(err.response?.data?.message)
        }
    }
    
    return (
    <>
      <form onSubmit={submit}>
        <label>email:</label>
        <input
          type="email"
          id="email"
          name="email"
          required
          onChange={handleChange}
        ></input>
        <br />
        <label>Password:</label>
        <input
          type="password"
          id="password"
          name="password"
          required
          onChange={handleChange}
        ></input>
        <br />
        <input type='submit' value="submit" />
        <br />
      </form>
    </>
  );
}

export default Login