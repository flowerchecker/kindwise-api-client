import click
from kindwise import PlantApi, InsectApi, MushroomApi

BACKENDS = {'plant': PlantApi, 'insect': InsectApi, 'mushroom': MushroomApi}


@click.command()
@click.argument('image_path', type=click.Path(exists=True))
@click.argument('backend', type=click.Choice(BACKENDS.keys()), default='plant')
@click.option('--api_key', envvar='KINDWISE_API_KEY', help='Your Kindwise API key')
def identify(backend, image_path, api_key):
    """
    Create an identification by specifying the path to an image and the desired backend.

    \b
    BACKEND: Choose from 'plant', 'insect', or 'mushroom'
    IMAGE_PATH: Path to the image file for identification
    """
    if backend not in BACKENDS:
        click.echo(f"Invalid backend: {backend}. Please choose from 'plant', 'insect', or 'mushroom'.")
        return

    api_class = BACKENDS[backend]

    try:
        api = api_class(api_key=api_key)
    except ValueError as e:
        click.echo(f"Error initializing API: {e}")
        return

    click.echo(f"Identifying image using {backend} backend...")
    try:
        identification = api.identify(image_path)
        click.echo(f"Identification result: {identification}")
    except Exception as e:
        click.echo(f"Error during identification: {e}")


@click.group()
def cli():
    pass


cli.add_command(identify)

if __name__ == '__main__':
    cli()
