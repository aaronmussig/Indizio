import os
import shutil
import sys
from typing import Optional

import dash
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from indizio import __version__
from indizio.components.layout.message import LayoutMessage
from indizio.components.layout.navbar import NavBar
from indizio.components.layout.reload import LayoutReload
from indizio.config import TMP_DIR
from indizio.models.common.logging import LogLevel
from indizio.store.active_stores import ACTIVE_STORES
from indizio.util.log import hide_logs
from indizio.util.log import log

# Load extra layouts
cyto.load_extra_layouts()

# Create the CLI application
app = typer.Typer(add_completion=False)


@app.command()
def main(
        logging: Optional[LogLevel] = LogLevel.INFO,
        debug: bool = False,
        port: int = 9001,
        host: str = 'localhost'
):
    # Hide non-critical messages from third-party packages
    try:
        hide_logs('werkzeug')
        cli = sys.modules['flask.cli']
        cli.show_server_banner = lambda *x: None
    except Exception:
        pass

    # Store the logging level in the global context
    os.environ["INDIZIO_LOG"] = str(logging.value)

    # Create the temporary directory used by Indizio for storing files
    TMP_DIR.mkdir(exist_ok=True)

    try:
        log(f'Indizio [bold blue]v{__version__}[/bold blue]')
        log(f'Writing temporary files to: {TMP_DIR.as_posix()}', level=LogLevel.DEBUG)

        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
        ) as progress:
            progress.add_task(description="Starting server...", total=None)

            # Create the Dash application
            dash_app = dash.Dash(
                __name__,
                use_pages=True,
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.JOURNAL, dbc.icons.FONT_AWESOME],
            )
            hide_logs('dash.dash')

            # Create the default layout
            dash_app.layout = dbc.Container(
                className="container-main",
                style={
                    "paddingLeft": 0,
                    "paddingRight": 0
                },
                fluid=True,
                children=
                [
                    # Future Stores will need to be declared here
                    *ACTIVE_STORES,

                    # Add the default page content
                    NavBar(debug),
                    LayoutMessage(),
                    LayoutReload(),
                    dbc.Container(
                        fluid=True,
                        children=
                        [
                            dash.page_container,
                        ]
                    )
                ]
            )

        log(f'To access Indizio, visit [link]http://{host}:{port}[/link]')
        dash_app.run(debug=debug, host=host, port=port)

    finally:
        if debug:
            log(f'Temporary files are not removed in debug mode: {TMP_DIR.as_posix()}')
        else:
            log('Cleaning up temporary files.', level=LogLevel.DEBUG)
            try:
                shutil.rmtree(TMP_DIR.as_posix())
            except Exception as e:
                log(f'Unable to remove temporary files: {e}', level=LogLevel.ERROR)


if __name__ == "__main__":
    app()
