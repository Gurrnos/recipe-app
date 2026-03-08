import { useState, useEffect } from "react";
import Axios from "axios";
import RecipeDisplay from "../components/RecipeDisplay";

const Account = () => {
    const [favoritedRecipes, setFavoritedRecepies] = useState([]);
    const [yourRecipes, setYourRecipes] = useState([]);
    const [username, setUsername] = useState("");
    const [passwordData, setPasswordData] = useState({
        old_passw: "",
        new_passw: ""
    });
    const [usernameData, setUsernameData] = useState({
        new_username: ""
    });

    useEffect(() => {
        auth();
        getFavorited();
        getOwnRecipes();
    }, []);

    const auth = async () => {
        try {
            const res = await Axios.post("/api/authenticate", { withCredentials: true });

            setUsername(res.data.username);
        } catch (err) {
            window.location.href = "/login";
        }
    }

    const getFavorited = async () => {
        try {
            const res = await Axios.get("/api/users/getFavorites", { withCredentials: true });
            
            const recipeData = res.data.map((recipe) => ({
                rid: recipe.rid,
                name: recipe.recipename,
                description: recipe.description
            }));

            setFavoritedRecepies(recipeData);
        } catch (err) {
            alert(err.response?.data?.message);
        }
    }

    const getOwnRecipes = async () => {
        try {
            const res = await Axios.get("/api/users/getUserRecipes/", { withCredentials: true, params: { own: true } });
            
            const recipeData = res.data.map((recipe) => ({
                rid: recipe.rid,
                name: recipe.recipename,
                description: recipe.description
            }));

            setYourRecipes(recipeData);
        } catch (err) {
            alert(err.response?.data?.message);
        }
    }

    function handleChange (e, type) {
        const {name, value} = e.target;

        if (type == "password") {
            setPasswordData((prevState) => ({
            ...prevState,
            [name]: value
            }));
        } else {
            setUsernameData((prevState) => ({
            ...prevState,
            [name]: value
            }));
        }

    }

    const updateData = async (e, mode) => {
        e.preventDefault();

        let data = {};
        let url = "";

        if (mode == "passw") {
            data = {
                ...passwordData
            };
            url = "changePassw"
        } else {
            data = {
                ...usernameData
            };
            url = "changeUsername"
        }


        try {
            const response = await Axios.put(`api/${url}`, data, { withCredentials: true });

            if (mode == "passw") {
                setPasswordData({old_passw: '', new_passw: ''});
            } else {
                setUsernameData({new_username: ''});
            }

            alert(response?.data?.message);

            auth();
        } catch (err) {
            alert(err.response?.data?.message);
        }
    }

    return(
        <>
            <h1>Account page</h1>

            <h2>Hello {username}</h2>

            <h2>Your favorited recepies:</h2>
            {favoritedRecipes.map((recipe) => (
                <RecipeDisplay
                    key={recipe.rid}
                    rid={recipe.rid}
                    name={recipe.name}
                    description={recipe.description}
                />
            ))}

            <h2>Your recipes:</h2>
            {yourRecipes.map((recipe) => (
                <RecipeDisplay
                    key={recipe.rid}
                    rid={recipe.rid}
                    name={recipe.name}
                    description={recipe.description}
                />
            ))}
            <h2>Change password</h2>
            <form onSubmit={(e) => updateData(e, "passw")}>
                <label>Old password:</label>
                <input
                    type="password"
                    id="password"
                    name="old_passw"
                    required
                    value={passwordData.old_passw}
                    onChange={(e) => handleChange(e, "password")}
                />
                <br />
                <label>New password:</label>
                <input
                    type="password"
                    id="password"
                    name="new_passw"
                    required
                    value={passwordData.new_passw}
                    onChange={(e) => handleChange(e, "password")}
                />
                <br />
                <input type='submit' value="submit" />
                <br />
            </form>

            <h2>Change username</h2>
            <form onSubmit={(e) => updateData(e, "username")}>
                <label>New username:</label>
                <input
                    type="text"
                    id="password"
                    name="new_username"
                    required
                    value={usernameData.new_username}
                    onChange={(e) => handleChange(e, "username")}
                />
                <br />
                <input type='submit' value="submit" />
                <br />
            </form>
        </>
    )
}

export default Account;