from fastapi import FastAPI

from vfdelivery.routes.customer_router import router as customer_router
from vfdelivery.routes.restaurant_router import router as restaurant_router

app = FastAPI(
    title='VFDelivery',
    description='Aplicação de food delivery focada no fluxo de pedidos e avaliações.',
    root_path='/api/v1'
)


app.include_router(customer_router)
app.include_router(restaurant_router)


@app.get('')
def root():
    return {'status': 'OK'}
