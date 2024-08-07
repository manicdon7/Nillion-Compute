import asyncio
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from asgiref.sync import async_to_sync
from .nillionSetup import NadaPublish
import logging

logger = logging.getLogger(__name__)

@require_GET
def store_program_view(request):
    # Extract parameters from the request
    age_int2 = request.GET.get('age_int2')
    location_int1 = request.GET.get('location_int1')
    match_gender_int = request.GET.get('match_gender_int')
    age_int1 = request.GET.get('age_int1')
    looking_for_gender_int = request.GET.get('looking_for_gender_int')

    # Validate and convert parameters
    try:
        age_int2 = int(age_int2)
        location_int1 = int(location_int1)
        match_gender_int = int(match_gender_int)
        age_int1 = int(age_int1)
        looking_for_gender_int = int(looking_for_gender_int)
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid input data"}, status=400)

    async def main():
        try:
            publish = NadaPublish(".env", "sample seed", "./MatchingAlgo.nada.bin", "MatchingAlgo")
            log, result = await publish.StoreProgram(
                "MatchParty", 
                {
                    "age_int2": age_int2, 
                    "location_int1": location_int1, 
                    "Match_gender_int": match_gender_int, 
                    "age_int1": age_int1, 
                    "looking_for_gender_int": looking_for_gender_int
                }, 
                verbose=True
            )
            return {"result": result, "log": log}
        except asyncio.TimeoutError:
            logger.error("Timeout occurred during StoreProgram execution")
            return {"error": "Timeout occurred during StoreProgram execution"}
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return {"error": f"An error occurred: {str(e)}"}

    # Use async_to_sync to run the async function in a sync context
    response = async_to_sync(main)()

    if "error" in response:
        return JsonResponse(response, status=500)
    
    return JsonResponse(response)
