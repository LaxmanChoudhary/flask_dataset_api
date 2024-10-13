from flask import request
from flask_restful import Resource
from dataset_api.api.schemas import VgSalesSchema
from dataset_api.models import VgSales
from dataset_api.commons.pagination import paginate
from sqlalchemy import desc, asc

QUERY_SORT = {
    'asc': asc,
    'desc': desc
}

class VgSalesList(Resource):
    def get(self):
        schema = VgSalesSchema(many=True)

        # filters = extract_filter_by(request.args)
        # query = VgSales.query.filter_by(**filters)

        _filter = get_filter(request.args)
        _order_by = set_order(request.args)

        query = VgSales.query.order_by(_order_by).filter(*_filter)
        return paginate(query, schema)

def set_order(args):
    if not 'sort_by' in args: return None

    by, fun = args["sort_by"].rsplit("_", maxsplit=1)
    if by and fun and fun in ['asc', 'desc']:
        if by == 'rank':
            return QUERY_SORT[fun](VgSales.rank)
        elif by == 'year':
            return QUERY_SORT[fun](VgSales.year)
        elif by == 'global_sales':
            return QUERY_SORT[fun](VgSales.global_sales)
    return None

def get_filter(args):
    _filter = []
    for k, v in args.items():
        if k == 'rank':
            op, value = v.rsplit("_", maxsplit=1)
            if not op or not value:
                continue
        elif k == 'name':
            _filter.append((VgSales.name == v))
        elif k == 'platform':
            _filter.append((VgSales.platform == v))
        elif k == 'year':
            op, value = v.rsplit("_", maxsplit=1)
            if op and value:
                res = _resolve_op(op, value, VgSales.year)
                res is not None and _filter.append(res)
        elif k == 'genre':
            _filter.append((VgSales.genre == v))
        elif k == 'publisher':
            _filter.append((VgSales.publisher == v))
        elif k == 'global_sales':
            op, value = v.rsplit("_", maxsplit=1)
            if op and value:
                res = _resolve_op(op, value, VgSales.global_sales)
                res is not None and _filter.append(res)
    return _filter

def _resolve_op(op, value, member):
    if op == 'gt':
        return (member > value)
    elif op == 'lt':
        return (member < value)
    elif op == 'gte':
        return (member >= value)
    elif op == 'lte':
        return (member <= value)
    else:
        return None

def extract_filter_by(args):
    columns = VgSales.metadata.tables["vg_sales"].columns.keys()
    filters = {}
    for k, v in args.items():
        if k in columns:
            filters[k] = v
    return filters
