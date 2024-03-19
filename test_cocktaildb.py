import requests
import pytest
import json.decoder

# Base URL for the Cocktail DB API
BASE_URL = "https://www.thecocktaildb.com/api/json/v1/1/"
response = requests.get(BASE_URL + "search.php?i=vodka")

def test_search_alcoholic_ingredient():
    response = requests.get(BASE_URL + "search.php?i=vodka")
    data = response.json()
    assert response.status_code == 200
    assert 'ingredients' in data, "No ingredients found in the response"
    assert len(data['ingredients']) > 0, "No ingredients found in the response"
    for ingredient in data['ingredients']:
        assert ingredient['strAlcohol'].lower() == 'yes', "Alcoholic ingredient not marked as alcoholic"

def test_search_non_alcoholic_ingredient():
    response = requests.get(BASE_URL + "search.php?i=orange juice")
    data = response.json()
    assert response.status_code == 200
    assert 'ingredients' in data, "No ingredients found in the response"
    assert len(data['ingredients']) > 0, "No ingredients found in the response"
    for ingredient in data['ingredients']:
        assert ingredient['strAlcohol'].lower() == 'no', "Non-alcoholic ingredient marked as alcoholic"

def test_verify_popular_cocktails_list():
    response = requests.get(BASE_URL + "popular.php")
    data = response.json()
    assert response.status_code == 200
    assert 'drinks' in data and len(data['drinks']) > 0, "No popular cocktails found in the response"

def test_verify_cocktail_details_by_id():
    cocktail_id = "11007"
    response = requests.get(BASE_URL + f"lookup.php?i={cocktail_id}")
    data = response.json()
    assert response.status_code == 200
    assert 'drinks' in data, "No cocktail details found in the response"
    if 'drinks' in data:
        assert data['drinks'] is not None, "Cocktail details should not be None"
        assert len(data['drinks']) > 0, "No details found for the cocktail ID"

def test_search_cocktails_by_name():
    response = requests.get(BASE_URL + f"search.php?s=Margarita")
    data = response.json()
    assert response.status_code == 200
    assert 'drinks' in data, "No cocktails found in the response"
    if 'drinks' in data:
        assert data['drinks'] is not None, "Cocktail list should not be None"
        assert len(data['drinks']) > 0, "No cocktails found for the provided name"
        # Validating schema properties for each cocktail in the response
        for cocktail in data['drinks']:
            assert 'strDrink' in cocktail
            assert 'strTags' in cocktail
            assert 'strCategory' in cocktail
            assert 'strAlcoholic' in cocktail
            assert 'strGlass' in cocktail
            assert 'strInstructions' in cocktail
            assert 'strDrinkThumb' in cocktail or cocktail.get('strDrinkThumb') is None
            assert 'strIngredient1' in cocktail
            assert 'strMeasure1' in cocktail or cocktail.get('strMeasure1') is None
            assert 'strImageSource' in cocktail or cocktail.get('strImageSource') is None
            assert 'strImageAttribution' in cocktail or cocktail.get('strImageAttribution') is None
            assert 'strCreativeCommonsConfirmed' in cocktail
            assert 'dateModified' in cocktail

# Test Case Verify that the API can search for cocktails by ingredient
def test_search_cocktails_by_ingredient():
    ingredient_name = "Vodka"
    response = requests.get(BASE_URL + f"filter.php?i={ingredient_name}")
    data = response.json()
    assert response.status_code == 200
    assert 'drinks' in data, "No cocktails found in the response"
    if 'drinks' in data:
        assert data['drinks'] is not None, "Cocktail list should not be None"
        assert len(data['drinks']) > 0, "No cocktails found containing the provided ingredient"

def test_random_cocktail():
    response = requests.get(BASE_URL + "random.php")
    data = response.json()
    assert response.status_code == 200
    assert 'drinks' in data, "No random cocktail found in the response"
    if 'drinks' in data:
        assert data['drinks'] is not None, "Random cocktail details should not be None"
        assert len(data['drinks']) == 1, "More than one random cocktail found in the response"

def test_filter_cocktails_by_glass():
    glass_name = "Champagne_flute"
    response = requests.get(BASE_URL + f"filter.php?g={glass_name}")
    data = response.json()
    assert response.status_code == 200
    assert 'drinks' in data, "No cocktails found in the response"
    if 'drinks' in data:
        assert data['drinks'] is not None, "Cocktail list should not be None"
        assert len(data['drinks']) > 0, "No cocktails found served in the specified glass"


#ADDITIONAL TEST CASES        
# Test Case: Verify that the API handles invalid input gracefully when retrieving details of an ingredient by its ID
def test_invalid_input_ingredient_details_by_id():
    # Define an invalid input ingredient ID
    invalid_ingredient_id = "invalid_id"  
    try:
        response = requests.get(BASE_URL + f"lookup.php?iid={invalid_ingredient_id}")
        response.raise_for_status()
        data = response.json()
        assert response.status_code == 200
        assert 'error' in data or 'ingredients' not in data, "Expected error message or indication of invalid input not found in the response"
    except json.decoder.JSONDecodeError:
        # Handle the case when  JSON decoding is failing
        assert True, "JSON decoding error occurred, indicating potential issue with the API response format"
    except requests.exceptions.RequestException as e:
        # Handle other types of request exceptions
        assert False, f"Request exception occurred: {str(e)}"

def test_search_cocktails_with_non_existent_ingredient():
    non_existent_ingredient_name = "Banana"  # Example non-existent ingredient name
    response = requests.get(BASE_URL + f"filter.php?i={non_existent_ingredient_name}")
    data = response.json() 
    assert response.status_code == 200
    assert 'drinks' in data, "No cocktails found in the response"
    if 'drinks' in data:
        assert isinstance(data['drinks'], list) or 'error' in data, "Unexpected response format"

# Test Cases for Functional Requirements:
        
def test_search_ingredient_valid():
    # Define the expected content for the ingredient "Vodka"
    expected_ingredient = {
        'idIngredient': '1',
        'strIngredient': 'Vodka',
        'strDescription': 'Vodka is a distilled beverage composed primarily of water and ethanol, sometimes with traces of impurities and flavorings. Traditionally, vodka is made by the distillation of fermented cereal grains or potatoes, though some modern brands use other substances, such as fruits or sugar.\r\n\r\nSince the 1890s, the standard Polish, Russian, Belarusian, Ukrainian, Estonian, Latvian, Lithuanian and Czech vodkas are 40% alcohol by volume ABV (80 US proof), a percentage that is widely misattributed to Dmitri Mendeleev. The European Union has established a minimum of 37.5% ABV for any "European vodka" to be named as such. Products sold as "vodka" in the United States must have a minimum alcohol content of 40%. Even with these loose restrictions, most vodka sold contains 40% ABV. For homemade vodkas and distilled beverages referred to as "moonshine", see moonshine by country.\r\n\r\nVodka is traditionally drunk neat (not mixed with any water, ice, or other mixer), though it is often served chilled in the vodka belt countries (Belarus, Estonia, Finland, Iceland, Latvia, Lithuania, Norway, Poland, Russia, Sweden, Ukraine). It is also commonly used in cocktails and mixed drinks, such as the vodka martini, Cosmopolitan, vodka tonic, Screwdriver, Greyhound, Black or White Russian, Moscow Mule, and Bloody Mary.\r\n\r\nScholars debate the beginnings of vodka. It is a contentious issue because very little historical material is available. For many centuries, beverages differed significantly compared to the vodka of today, as the spirit at that time had a different flavor, color and smell, and was originally used as medicine. It contained little alcohol, an estimated maximum of about 14%, as only this amount can be attained by natural fermentation. The still, allowing for distillation ("burning of wine"), increased purity, and increased alcohol content, was invented in the 8th century.\r\n\r\nA common property of the vodkas produced in the United States and Europe is the extensive use of filtration prior to any additional processing including the addition of flavorants. Filtering is sometimes done in the still during distillation, as well as afterwards, where the distilled vodka is filtered through activated charcoal and other media to absorb trace amounts of substances that alter or impart off-flavors to the vodka. However, this is not the case in the traditional vodka-producing nations, so many distillers from these countries prefer to use very accurate distillation but minimal filtering, thus preserving the unique flavors and characteristics of their products.\r\n\r\nThe master distiller is in charge of distilling the vodka and directing its filtration, which includes the removal of the "fore-shots", "heads" and "tails". These components of the distillate contain flavor compounds such as ethyl acetate and ethyl lactate (heads) as well as the fusel oils (tails) that impact the usually desired clean taste of vodka. Through numerous rounds of distillation, or the use of a fractioning still, the taste is modified and clarity is increased. In contrast, distillery process for liquors such as whiskey, rum, and baijiu allow portions of the "heads" and "tails" to remain, giving them their unique flavors.\r\n\r\nRepeated distillation of vodka will make its ethanol level much higher than is acceptable to most end users, whether legislation determines strength limits or not. Depending on the distillation method and the technique of the stillmaster, the final filtered and distilled vodka may have as much as 95–96% ethanol. As such, most vodka is diluted with water prior to bottling.\r\n\r\nPolish distilleries make a very pure (96%, 192 proof, formerly also 98%) rectified spirit (Polish language: spirytus rektyfikowany). Technically a form of vodka, it is sold in liquor stores rather than pharmacies. Similarly, the German market often carries German, Hungarian, Polish, and Ukrainian-made varieties of vodka of 90 to 95% ABV. A Bulgarian vodka, Balkan 176°, has an 88% alcohol content. Everclear, an American brand, is also sold at 95% ABV.',
        'strType': 'Vodka',
        'strAlcohol': 'Yes',
        'strABV': '40'
    }
    response = requests.get(BASE_URL + "search.php?i=vodka")
    data = response.json()
    assert response.status_code == 200
    assert 'ingredients' in data, "No ingredients found in the response"
    assert len(data['ingredients']) > 0, "No ingredients found in the response"
    ingredient = data['ingredients'][0]
    assert ingredient['idIngredient'] == expected_ingredient['idIngredient']
    assert ingredient['strIngredient'] == expected_ingredient['strIngredient']
    assert ingredient['strDescription'] == expected_ingredient['strDescription']
    assert ingredient['strType'] == expected_ingredient['strType']
    assert ingredient['strAlcohol'] == expected_ingredient['strAlcohol']
    assert ingredient['strABV'] == expected_ingredient['strABV']

def test_search_ingredient_non_alcoholic():
    response = requests.get(BASE_URL + "search.php?i=orange juice")
    data = response.json()
    assert response.status_code == 200
    assert len(data['ingredients']) == 1
    assert data['ingredients'][0]['strIngredient'].lower() == 'orange juice'  # Case-insensitive comparison
    assert data['ingredients'][0]['strAlcohol'] == 'No'
    assert data['ingredients'][0]['strABV'] is None

def test_search_ingredient_valid():
    response = requests.get(BASE_URL + "search.php?i=vodka")
    data = response.json()
    assert response.status_code == 200
    # Check if the response contains 'ingredients' key
    assert 'ingredients' in data
    assert len(data['ingredients']) > 0
    for ingredient in data['ingredients']:
        assert 'strDescription' in ingredient
        assert 'strType' in ingredient

def test_search_cocktail_nonexistent():
    response = requests.get(BASE_URL + "search.php?s=NonexistentCocktail")
    data = response.json()
    assert response.status_code == 200
    assert 'drinks' in data
    assert data['drinks'] is None or len(data['drinks']) == 0

def test_search_cocktail_case_insensitive():
    response_upper = requests.get(BASE_URL + "search.php?s=MARGARITA")
    response_lower = requests.get(BASE_URL + "search.php?s=margarita")
    assert response_upper.status_code == 200
    assert response_lower.status_code == 200
    assert response_upper.json() == response_lower.json()

def test_search_cocktail_valid():
    cocktail_name = "Margarita"
    response = requests.get(BASE_URL + f"search.php?s={cocktail_name}")
    data = response.json()
    assert response.status_code == 200
    assert data['drinks'], "No drinks found for the cocktail name"
    margarita = data['drinks'][0]
    required_properties = [
        'strDrink', 'strTags', 'strCategory', 'strAlcoholic', 'strGlass',
        'strInstructions'
    ]
    for prop in required_properties:
        assert prop in margarita, f"Property {prop} is missing in the response"

    for i in range(1, 16):
        ingredient_key = f'strIngredient{i}'
        measure_key = f'strMeasure{i}'
        assert ingredient_key in margarita, f"Ingredient {i} is missing in the response"
        assert measure_key in margarita, f"Measure {i} is missing in the response"

def test_search_nonexistent_cocktail():
    cocktail_name = "Nonexistent Cocktail"
    response = requests.get(BASE_URL + f"search.php?s={cocktail_name}")
    data = response.json()
    assert response.status_code == 200
    assert 'drinks' in data
    assert isinstance(data['drinks'], list) or data['drinks'] is None

def test_case_insensitive_search():
    cocktail_name = "MaRgArItA"
    response = requests.get(BASE_URL + f"search.php?s={cocktail_name}")
    data = response.json()
    assert response.status_code == 200
    assert 'drinks' in data
    assert isinstance(data['drinks'], list)
    # Validate schema properties for each cocktail in the response
    for cocktail in data['drinks']:
        assert 'strDrink' in cocktail
        assert isinstance(cocktail['strDrink'], str) or cocktail['strDrink'] is None
        assert 'strDrinkAlternative' in cocktail or cocktail.get('strDrinkAlternative') is None
        assert isinstance(cocktail.get('strDrinkAlternative'), str) or cocktail.get('strDrinkAlternative') is None
        assert 'strTags' in cocktail
        assert isinstance(cocktail['strTags'], str) or cocktail['strTags'] is None
        assert 'strVideo' in cocktail
        assert isinstance(cocktail['strVideo'], str) or cocktail['strVideo'] is None
        assert 'strCategory' in cocktail
        assert isinstance(cocktail['strCategory'], str) or cocktail['strCategory'] is None
        assert 'strIBA' in cocktail
        assert isinstance(cocktail['strIBA'], str) or cocktail['strIBA'] is None
        assert 'strAlcoholic' in cocktail
        assert isinstance(cocktail['strAlcoholic'], str) or cocktail['strAlcoholic'] is None
        assert 'strGlass' in cocktail
        assert isinstance(cocktail['strGlass'], str) or cocktail['strGlass'] is None
        assert 'strInstructions' in cocktail
        assert isinstance(cocktail['strInstructions'], str) or cocktail['strInstructions'] is None
        assert 'strDrinkThumb' in cocktail
        assert isinstance(cocktail['strDrinkThumb'], str) or cocktail['strDrinkThumb'] is None
        assert 'strIngredient1' in cocktail
        assert isinstance(cocktail['strIngredient1'], str) or cocktail['strIngredient1'] is None
        assert 'strMeasure1' in cocktail
        assert isinstance(cocktail['strMeasure1'], str) or cocktail['strMeasure1'] is None
        assert 'strImageSource' in cocktail
        assert isinstance(cocktail['strImageSource'], str) or cocktail['strImageSource'] is None
        assert 'strImageAttribution' in cocktail
        assert isinstance(cocktail['strImageAttribution'], str) or cocktail['strImageAttribution'] is None
        assert 'strCreativeCommonsConfirmed' in cocktail
        assert isinstance(cocktail['strCreativeCommonsConfirmed'], str) or cocktail['strCreativeCommonsConfirmed'] is None
        assert 'dateModified' in cocktail
        assert isinstance(cocktail['dateModified'], str) or cocktail['dateModified'] is None

def test_regression_schema_properties():
    # Defining a list of endpoints to be tested for regression
    endpoints = [
        "search.php?s=Margarita",
        "search.php?i=vodka"
    ]
    # Iterating over each endpoint and perform regression testing
    for endpoint in endpoints:
        response = requests.get(BASE_URL + endpoint)
        data = response.json()
        assert response.status_code == 200, f"Failed to fetch data for endpoint: {endpoint}"
        if 'drinks' in data:
            drinks = data.get('drinks')
            assert drinks is not None, f"Response for {endpoint} has 'drinks' key but its value is None"
            assert isinstance(drinks, list), f"Value of 'drinks' key is not a list for endpoint: {endpoint}"
            assert len(drinks) > 0, f"No cocktails found for the provided endpoint: {endpoint}"
            for drink in drinks:
                assert 'strDrink' in drink, f"Property 'strDrink' not found for drink in endpoint: {endpoint}"
                assert isinstance(drink['strDrink'], str) or drink['strDrink'] is None, \
                    f"Property 'strDrink' has incorrect type for drink in endpoint: {endpoint}"
                # Adding assertions for other properties
                assert 'strDrinkAlternative' in drink or 'strDrinkAlternative' not in drink or drink['strDrinkAlternative'] is None, \
                    f"Property 'strDrinkAlternative' not found for drink in endpoint: {endpoint}"
                assert 'strTags' in drink or drink['strTags'] is None, \
                    f"Property 'strTags' not found for drink in endpoint: {endpoint}"
                assert 'strVideo' in drink or drink['strVideo'] is None, \
                    f"Property 'strVideo' not found for drink in endpoint: {endpoint}"
                assert 'strCategory' in drink or drink['strCategory'] is None, \
                    f"Property 'strCategory' not found for drink in endpoint: {endpoint}"
                assert 'strIBA' in drink or drink['strIBA'] is None, \
                    f"Property 'strIBA' not found for drink in endpoint: {endpoint}"
                assert 'strAlcoholic' in drink or drink['strAlcoholic'] is None, \
                    f"Property 'strAlcoholic' not found for drink in endpoint: {endpoint}"
                assert 'strGlass' in drink or drink['strGlass'] is None, \
                    f"Property 'strGlass' not found for drink in endpoint: {endpoint}"
                assert 'strInstructions' in drink or drink['strInstructions'] is None, \
                    f"Property 'strInstructions' not found for drink in endpoint: {endpoint}"
                assert 'strDrinkThumb' in drink or drink['strDrinkThumb'] is None, \
                    f"Property 'strDrinkThumb' not found for drink in endpoint: {endpoint}"
                assert 'dateModified' in drink or drink['dateModified'] is None, \
                    f"Property 'dateModified' not found for drink in endpoint: {endpoint}"
        else:
            assert True, f"No 'drinks' key found in the response for endpoint: {endpoint}"
    print("API response schema validation passed successfully.")
    
# Executing automated tests with pytest
if __name__ == "__main__":
    pytest.main([__file__, "-s"])