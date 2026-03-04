import { useState, useEffect } from "react"
import Axios from "axios";
import RecipeDisplay from "../components/RecipeDisplay";

const Home = () => {

    const [recipies, setRecipies] = useState([]);

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

            setRecipies(recipeData);

        } catch (err) {
            alert(err.response?.data?.message);
            console.log(err);
        }
    }

    return (
        <>
            <h2>Home page</h2>

            {recipies.map((recipe) => (
                <RecipeDisplay
                    key={recipe.rid}
                    rid={recipe.rid}
                    name={recipe.name}
                    description={recipe.description}
                    favoriteCount={recipe.favoriteCount}
                />
            ))}
        </>
    )
}

export default Home