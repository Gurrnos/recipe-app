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
    const [recipeData, setRecipeData] = useState({
        recipename: "",
        description: "",
        ispublic: 0,
        ingredients: [],
        steps: []
    });
    const initialRecipeData = {
        recipename: "",
        description: "",
        ispublic: 0,
        ingredients: [],
        steps: []
    };

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

    // Handle changes for inputs (recipename, description, ispublic)
    const handleRecipeChange = (e) => {
        const { name, value, type, checked } = e.target;
        setRecipeData((prevState) => ({
            ...prevState,
            [name]: type === 'checkbox' ? (checked ? 1 : 0) : value
        }));
    };

    // Handle changes for individual ingredient fields
    const updateIngredient = (index, field, value) => {
        const updatedIngredients = [...recipeData.ingredients];
        updatedIngredients[index][field] = value;
        setRecipeData((prevState) => ({
            ...prevState,
            ingredients: updatedIngredients
        }));
    };

    // Add a new ingredient form
    const addIngredient = () => {
        setRecipeData((prevState) => ({
            ...prevState,
            ingredients: [...prevState.ingredients, { name: "", type: "", amount: "" }]
        }));
    };

    // Remove an ingredient
    const removeIngredient = (index) => {
        const updatedIngredients = recipeData.ingredients.filter((_, i) => i !== index);
        setRecipeData((prevState) => ({
            ...prevState,
            ingredients: updatedIngredients
        }));
    };

    // Handle changes for steps
    const updateStep = (index, value) => {
        const updatedSteps = [...recipeData.steps];
        updatedSteps[index] = value;
        setRecipeData((prevState) => ({
            ...prevState,
            steps: updatedSteps
        }));
    };

    // Add a new step field
    const addStep = () => {
        setRecipeData((prevState) => ({
            ...prevState,
            steps: [...prevState.steps, ""]
        }));
    };

    // Remove a step
    const removeStep = (index) => {
        const updatedSteps = recipeData.steps.filter((_, i) => i !== index);
        setRecipeData((prevState) => ({
            ...prevState,
            steps: updatedSteps
        }));
    };

     const resetForm = () => {
        setRecipeData(initialRecipeData);
    };

    const createRecipe = async (e) => {
        e.preventDefault();

        const data = {
            ...recipeData
        };

        console.log(data);

        try {
            await Axios.post("/api/createRecipe", data, { withCredentials: true });

            alert("Successfully created recipe");
            resetForm();
        } catch (err) {
            alert(err.response?.data?.message);
        }
    }

    const deleteAccount = async () => {
        try {
            await Axios.delete("/api/deleteAccount", {withCredentials: true});

            alert("Deleted account");
            
        } catch (err) {
            alert(err.response?.data?.message);
        }
    }

    return(
        <>
            <h1>Account page</h1>

            <h2>Hello {username}</h2>
            <button onClick={deleteAccount}>Delete account (irreversible)</button>

            <h2>Your favorited recepies:</h2>
            <div className="recipes-grid">
            {favoritedRecipes.map((recipe) => (
                <RecipeDisplay
                    key={recipe.rid}
                    rid={recipe.rid}
                    name={recipe.name}
                    description={recipe.description}
                />
            ))}
            </div>

            <h2>Your recipes:</h2>
            <div className="recipes-grid">
                {yourRecipes.map((recipe) => (
                    <RecipeDisplay
                        key={recipe.rid}
                        rid={recipe.rid}
                        name={recipe.name}
                        description={recipe.description}
                    />
                ))}
            </div>
            <h2>Create new recipe:</h2>
            <form onSubmit={createRecipe}>
                <div>
                <label htmlFor="recipename">Recipe Name:</label>
                <input
                    type="text"
                    id="recipename"
                    name="recipename"
                    value={recipeData.recipename}
                    onChange={handleRecipeChange}
                />
            </div>
            <div>
                <label htmlFor="description">Description:</label>
                <textarea
                    id="description"
                    name="description"
                    value={recipeData.description}
                    onChange={handleRecipeChange}
                ></textarea>
            </div>
            <div>
                <label htmlFor="ispublic">Is Public:</label>
                <input
                    type="checkbox"
                    id="ispublic"
                    name="ispublic"
                    checked={recipeData.ispublic}
                    onChange={handleRecipeChange}
                />
            </div>

            <div>
                <h3>Ingredients:</h3>
                <button type="button" onClick={addIngredient}>Add Ingredient</button>
                {recipeData.ingredients.map((ingredient, index) => (
                    <div key={index}>
                        <label>Ingredient Name:</label>
                        <input
                            type="text"
                            value={ingredient.name}
                            onChange={(e) => updateIngredient(index, 'name', e.target.value)}
                        />
                        <label>Ingredient Type:</label>
                        <input
                            type="text"
                            value={ingredient.type}
                            onChange={(e) => updateIngredient(index, 'type', e.target.value)}
                        />
                        <label>Amount:</label>
                        <input
                            type="text"
                            value={ingredient.amount}
                            onChange={(e) => updateIngredient(index, 'amount', e.target.value)}
                        />
                        <button type="button" onClick={() => removeIngredient(index)}>Remove Ingredient</button>
                    </div>
                ))}
            </div>

            <div>
                <h3>Steps:</h3>
                <button type="button" onClick={addStep}>Add Step</button>
                {recipeData.steps.map((step, index) => (
                    <div key={index}>
                        <label>Step {index + 1}:</label>
                        <input
                            type="text"
                            value={step}
                            onChange={(e) => updateStep(index, e.target.value)}
                        />
                        <button type="button" onClick={() => removeStep(index)}>Remove Step</button>
                    </div>
                ))}
            </div>

            <button type="submit">Submit</button>
            </form>

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