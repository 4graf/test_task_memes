from sqlalchemy import Select

from app.core.mem.domain.utils.mem_filter_params import MemFilterParams


class MemFilter:
    """
    Фильтр для запросов мемов.
    """

    @classmethod
    def filter_query(cls, query: Select, mem_filter_params: MemFilterParams) -> Select:
        offset = (mem_filter_params.page - 1) * mem_filter_params.per_page
        return query.offset(offset).limit(mem_filter_params.per_page)
