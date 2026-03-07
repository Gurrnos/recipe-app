import "../styles/RecipeDisplay.css"; 

const RecipeDisplay = ({ rid, name, description, favoriteCount }) => {
    
    const handleClick = () => {
        console.log("Clicked recipe ID: ", rid);
    }

    return (
        <div className="recipe-card" onClick={handleClick}>
            <h2 className="recipe-title">{name}</h2>
            <p className="recipe-description">{description}</p>
            {favoriteCount && (<p>Recipe favorite count: {favoriteCount}</p>) || <></>}
        </div>
    )
}

export default RecipeDisplay;