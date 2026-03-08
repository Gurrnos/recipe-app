import "../styles/RecipeDisplay.css"; 
import Axios from "axios";

const RecipeDisplay = ({ rid, name, description, favoriteCount }) => {
    
    const handleDelete = async () => {
        try {  
            await Axios.delete("/api/deleteRecipe/", {params: {p_rid: rid} , withCredentials: true});

            alert("Deleted recipe");
        } catch (err) {
            alert(err.response?.data?.message);
        }
        console.log("Clicked recipe ID: ", rid);
    }

    return (
        <div className="recipe-card">
            <h2 className="recipe-title">{name}</h2>
            <p className="recipe-description">{description}</p>
            {favoriteCount && (<p>Recipe favorite count: {favoriteCount}</p>) || <></>}
            <button onClick={handleDelete}>Delete recipe (requires ownership)</button>
        </div>
    )
}

export default RecipeDisplay;