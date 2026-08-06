from fastapi import FastAPI

from vfdelivery.routes.customer_router import router as customer_router

app = FastAPI(
    title='VFDelivery',
    description='Aplicação de food delivery focada no fluxo de pedidos e avaliações.',
    root_path='/api/v1'
)


app.include_router(customer_router)


@app.get('')
def root():
    return {'status': 'OK'}
