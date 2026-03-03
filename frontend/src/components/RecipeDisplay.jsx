const RecipeDisplay = (recipe) => {
    return (
        <div key={recipe.rid}>
            <p>Component start...</p>
            <p>Recipe name: {recipe.name}</p>
            <p>Recipe description: {recipe.description} </p>
            <p>Recipe favorite count: {recipe.favoriteCount}</p>
            <br />
        </div>
    )
}

export default RecipeDisplay;