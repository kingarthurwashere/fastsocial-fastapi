from typing import Optional
from app.schemas import GeminiResult, PlanRow

class CanvaService:
    @staticmethod
    async def generate_image(plan: PlanRow, gem: GeminiResult) -> Optional[str]:
        """Placeholder for Canva Magic Design or your generator.
        Return a hosted image URL. For now, return None.
        """
        return None
