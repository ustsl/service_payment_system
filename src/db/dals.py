import uuid

from sqlalchemy import desc, func, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta

from src.settings import PAGINATION_PAGE_SIZE

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class BaseDAL:
    def __init__(self, db_session: AsyncSession, model: DeclarativeMeta):
        self.db_session = db_session
        self.model = model

    async def create(self, **data):
        try:
            new_prompt = self.model(**data)
            self.db_session.add(new_prompt)
            await self.db_session.flush()
            return new_prompt
        except Exception as e:
            await self.db_session.rollback()
            error_msg = f"Error creating prompt: {str(e)}"
            return {"error": error_msg}

    async def list(
        self,
        page_size: int = PAGINATION_PAGE_SIZE,
        offset: int = 0,
        order_param="uuid",
        filters: dict = {},
    ):
        try:
            query = (
                select(self.model)
                .order_by(desc(getattr(self.model, order_param)))
                .limit(page_size)
                .offset(offset)
            )

            # Apply filters
            for attr, value in filters.items():
                query = query.where(getattr(self.model, attr) == value)

            db_query_result = await self.db_session.execute(query)
            result = db_query_result.scalars().all()

            total_count_query = select(func.count()).select_from(self.model)
            total_count_result = await self.db_session.execute(total_count_query)
            total_count = total_count_result.scalar()

            return {"result": result, "total": total_count}
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    async def get(self, uuid: str):

        try:
            query = select(self.model).where(self.model.uuid == uuid)
            db_query_result = await self.db_session.execute(query)
            res = db_query_result.scalar_one()
            return res
        except NoResultFound:
            return {"error": "Not found", "status": 404}
        except Exception as e:
            await self.db_session.rollback()
            return {"error": f"Error: {str(e)}", "status": 500}

    async def update(self, uuid: uuid.UUID, **kwargs):
        try:
            query = (
                update(self.model)
                .where(self.model.uuid == uuid)
                .values(**kwargs)
                .execution_options(synchronize_session="fetch")
            )
            await self.db_session.execute(query)
            await self.db_session.commit()
            return {"success": "Updated successfully"}
        except Exception as e:
            await self.db_session.rollback()
            return {"error": f"Error updating: {str(e)}"}

    async def delete(self, id: uuid.UUID):
        try:
            query = (
                update(self.model).where(self.model.uuid == id).values(is_deleted=True)
            )
            await self.db_session.execute(query)
            await self.db_session.commit()
            return {"success": "Prompt deleted successfully"}
        except Exception as e:
            await self.db_session.rollback()
            return {"error": f"Error deleting prompt: {str(e)}"}
