import { useState, useEffect } from "react";
import Axios from "axios";

const DetailedRecipe = () => {
    const [recipeData, setRecipeData] = useState({
        recipename: "",
        description: "",
        ispublic: 0, // Default value (0 or 1 for checkbox)
        ingredients: [],
        steps: []
    });

    useEffect(() => {
        getRecipe();
    }, []);

    const url = window.location.href;
    const v_rid = url.charAt(url.length - 1);  // Assuming the recipe ID is the last character in the URL

    const getRecipe = async () => {
        try {
            const res = await Axios.get("/api/getRecipeDetailed/", { params: { rid: v_rid } });

            setRecipeData(res.data);   // Set the data from the API to state
        } catch (err) {
            alert(err.response?.data?.message || "Something went wrong!");
        }
    };

    // Handle changes for inputs (recipename, description, ispublic)
    const handleRecipeChange = (e) => {
        const { name, value, type, checked } = e.target;
        setRecipeData((prevState) => ({
            ...prevState,
            [name]: type === "checkbox" ? (checked ? 1 : 0) : value
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

    // Handle form submission (update recipe)
    const updateRecipe = async (e) => {
        e.preventDefault();

        const data = {
            ...recipeData
        };

        console.log(data);

        try {
            await Axios.put("/api/editRecipe/", data, { withCredentials: true, params: {rid: v_rid} });
            alert("Recipe updated successfully!");
        } catch (err) {
            alert(err.response?.data?.message);
        }
    };

    return (
        <>
            <h1>Detailed recipe for {recipeData.recipename || "Loading..."}</h1>

            <h3>Description:</h3>
            <p>{recipeData.description || "Loading..."}</p>

            <h3>Ingredients:</h3>
            <ul>
                {recipeData.ingredients && recipeData.ingredients.length > 0 ? (
                    recipeData.ingredients.map((ingredient, index) => (
                        <li key={index}>
                            <strong>{ingredient.name}</strong> ({ingredient.amount}) - {ingredient.type}
                        </li>
                    ))
                ) : (
                    <p>No ingredients available</p>
                )}
            </ul>

            <h3>Steps:</h3>
            <ol>
                {recipeData.steps && recipeData.steps.length > 0 ? (
                    recipeData.steps.map((step, index) => (
                        <li key={index}>
                            {step}
                        </li>
                    ))
                ) : (
                    <p>No steps available</p>
                )}
            </ol>

            <h3>Edit this recipe:</h3>
            <form onSubmit={updateRecipe}>
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
                        checked={recipeData.ispublic === 1}
                        onChange={handleRecipeChange}
                    />
                </div>

                <div>
                    <h3>Ingredients:</h3>
                    <button type="button" onClick={addIngredient}>
                        Add Ingredient
                    </button>
                    {recipeData.ingredients.map((ingredient, index) => (
                        <div key={index}>
                            <label>Ingredient Name:</label>
                            <input
                                type="text"
                                value={ingredient.name}
                                onChange={(e) =>
                                    updateIngredient(index, "name", e.target.value)
                                }
                            />
                            <label>Ingredient Type:</label>
                            <input
                                type="text"
                                value={ingredient.type}
                                onChange={(e) =>
                                    updateIngredient(index, "type", e.target.value)
                                }
                            />
                            <label>Amount:</label>
                            <input
                                type="text"
                                value={ingredient.amount}
                                onChange={(e) =>
                                    updateIngredient(index, "amount", e.target.value)
                                }
                            />
                            <button type="button" onClick={() => removeIngredient(index)}>
                                Remove Ingredient
                            </button>
                        </div>
                    ))}
                </div>

                <div>
                    <h3>Steps:</h3>
                    <button type="button" onClick={addStep}>
                        Add Step
                    </button>
                    {recipeData.steps.map((step, index) => (
                        <div key={index}>
                            <label>Step {index + 1}:</label>
                            <input
                                type="text"
                                value={step}
                                onChange={(e) => updateStep(index, e.target.value)}
                            />
                            <button type="button" onClick={() => removeStep(index)}>
                                Remove Step
                            </button>
                        </div>
                    ))}
                </div>

                <button type="submit">Update Recipe</button>
            </form>
        </>
    );
};

export default DetailedRecipe;