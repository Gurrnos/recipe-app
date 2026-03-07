import { useState, useEffect } from "react"
import Axios from "axios";
import RecipeDisplay from "../components/RecipeDisplay";
import "../styles/Home.css"

const Home = () => {
    const [recipes, setRecipes] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getTopRecepies();
    }, []);

    const getTopRecepies = async () => {
        try {
            const res = await Axios.get("api/getTopRecepies");

            const recipeData = res.data.map((recipe) => ({
                rid: recipe.rid,
                name: recipe.recipename,
                description: recipe.description,
                favoriteCount: recipe.favoriteCount
            }));

            console.log(recipeData);

            setRecipes(recipeData);

        } catch (err) {
            alert(err.response?.data?.message);
            console.log(err);
        }
         finally {
            setLoading(false);
        }
    }

    if (loading) return <div>Loading recipes...</div>;

    return (
        <div className="home-container">
            <h2>All Recipes</h2>
            {recipes.length === 0 ? (
                <p>No recipes found.</p>
            ) : (
                <div className="recipes-grid">
                    {recipes.map((recipe) => (
                        <RecipeDisplay
                            key={recipe.rid}
                            rid={recipe.rid}
                            name={recipe.name}
                            description={recipe.description}
                            favoriteCount={recipe.favoriteCount}
                        />
                    ))}
                </div>
            )}
        </div>
    )
}

export default Home;