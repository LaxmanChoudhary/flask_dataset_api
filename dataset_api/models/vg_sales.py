from dataset_api.extensions import db


class VgSales(db.Model):
    __tablename__ = "vg_sales"

    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer)
    name = db.Column(db.String(80), nullable=False)
    platform = db.Column(db.String(80))
    year = db.Column(db.Integer)
    genre = db.Column(db.String(80))
    publisher = db.Column(db.String(80))
    na_sales = db.Column(db.Float)
    eu_sales = db.Column(db.Float)
    jp_sales = db.Column(db.Float)
    other_sales = db.Column(db.Float)
    global_sales = db.Column(db.Float)

    def __repr__(self):
        return f"{self.name} by {self.publisher}"

    def filter_columns(self):
        return self.metadata.tables["vg_sales"].columns.keys()
