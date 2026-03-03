const RecipeDisplay = ({
    rid,
    name,
    description,
    favoriteCount
}) => {
    
    const handleClick = () => {
        console.log("Clicked id: ", rid);
    }

    return (
        <div onClick={handleClick}>
            <p>Component start...</p>
            <p>Recipe name: {name}</p>
            <p>Recipe description: {description} </p>
            <p>Recipe favorite count: {favoriteCount}</p>
            <br />
        </div>
    )
}

export default RecipeDisplay;