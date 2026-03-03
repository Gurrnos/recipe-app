import { useState, useEffect } from 'react';
import Axios from 'axios';
import '../App.css'

const Signup = () => {
  const [userData, setUserData] = useState({
    username: "",
    email: "",
    password: ""
  });

  function handleChange (e) {
    const {name, value} = e.target;

    setUserData((prevState) => ({
      ...prevState,
      [name]: value
    }));
  }

  async function submit (e) {
    e.preventDefault();

    const data = {
      ...userData
    };

    console.log(data)

    try {
      await Axios.post("/api/signup", data);

      window.location.href = "/";

    } catch (err) {
      alert(err.response?.data?.message)
    }
  }

  return (
    <>
      <form onSubmit={submit}>
        <label>username:</label>
        <input
          type="username"
          id="username"
          name="username"
          required
          onChange={handleChange}
        ></input>
        <br />
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
  )
}

export default Signup
