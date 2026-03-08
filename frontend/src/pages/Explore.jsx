import Axios from "axios";
import { useEffect, useState } from "react"
import RecipeDisplay from "../components/RecipeDisplay";

const Explore = () => {
    const [recipes, setRecipes] = useState([]);
    const [searchData, setSearchData] = useState({
        recipename: "",
        ingredients: [],
        exclude_own: false
    });

    const [ingredientInput, setIngredientInput] = useState("");

    // handle recipe name + checkbox
    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;

        setSearchData((prev) => ({
            ...prev,
            [name]: type === "checkbox" ? checked : value
        }));
    };

    // add ingredient
    const addIngredient = () => {
        if (ingredientInput.trim() === "") return;

        setSearchData((prev) => ({
            ...prev,
            ingredients: [...prev.ingredients, ingredientInput.trim()]
        }));

        setIngredientInput("");
    };

    // remove ingredient
    const removeIngredient = (index) => {
        const updated = searchData.ingredients.filter((_, i) => i !== index);

        setSearchData((prev) => ({
            ...prev,
            ingredients: updated
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const res = await Axios.post("/api/getRecipes", searchData, { withCredentials: searchData.exclude_own });

            setRecipes(res.data);
        } catch (err) {
            alert(err.response?.data?.message || "Search failed");
        }
    };

    return (
        <>
        <form onSubmit={handleSubmit}>

            <h2>Search Recipes</h2>

            {/* Recipe name search */}
            <div>
                <label>Recipe Name:</label>
                <input
                    type="text"
                    name="recipename"
                    value={searchData.recipename}
                    onChange={handleChange}
                    placeholder="Search recipe..."
                />
            </div>

            {/* Ingredient input */}
            <div>
                <label>Add Ingredient:</label>
                <input
                    type="text"
                    value={ingredientInput}
                    onChange={(e) => setIngredientInput(e.target.value)}
                    placeholder="e.g. chicken"
                />
                <button type="button" onClick={addIngredient}>
                    Add
                </button>
            </div>

            {/* Ingredient list */}
            <div>
                <h4>Ingredients:</h4>
                {searchData.ingredients.map((ing, index) => (
                    <div key={index}>
                        {ing}
                        <button
                            type="button"
                            onClick={() => removeIngredient(index)}
                        >
                            Remove
                        </button>
                    </div>
                ))}
            </div>

            {/* Exclude own recipes */}
            <div>
                <label>
                    <input
                        type="checkbox"
                        name="exclude_own"
                        checked={searchData.exclude_own}
                        onChange={handleChange}
                    />
                    Exclude my recipes
                </label>
            </div>

            <button type="submit">Search</button>

        </form>

        <h1>Result</h1>
        <div className="recipes-grid">
                    {recipes.map((recipe) => (
                        <RecipeDisplay
                            key={recipe.rid}
                            rid={recipe.rid}
                            name={recipe.recipename}
                            description={recipe.description}
                            favoriteCount={recipe.favoriteCount}
                        />
                    ))}
                </div>
        </>
    )
}

export default Explore