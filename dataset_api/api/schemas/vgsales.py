from dataset_api.models import VgSales
from dataset_api.extensions import ma, db


class VgSalesSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)

    class Meta:
        model = VgSales
        sqla_session = db.session
        load_instance = True
