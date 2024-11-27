import pytest
import grass.script as gs


@pytest.fixture
def setup_maps(tmp_path):
    """Set up a GRASS session and create test raster maps."""
    # Initialize GRASS project
    project = "r_coin_project"
    gs.create_project(tmp_path, project)
    with gs.setup.init(tmp_path / project) as session:
        # Set the region
        gs.run_command(
            "g.region",
            n=3,
            s=0,
            e=3,
            w=0,
            res=1,
            env=session.env,
        )

        # Create the raster maps
        # map1:
        # 1 1 2
        # 1 2 3
        # 2 2 3
        gs.mapcalc(
            "map1 = "
            "if(row() == 1 && col() <= 2, 1, "
            "if(row() == 1 && col() == 3, 2, "
            "if(row() == 2 && col() == 1, 1, "
            "if(row() == 2 && col() == 2, 2, "
            "if(row() == 2 && col() == 3, 3, "
            "if(row() == 3 && col() <= 2, 2, 3))))))",
            overwrite=True,
            env=session.env,
        )

        # map2:
        # 1 2 2
        # 2 1 3
        # 3 3 3
        gs.mapcalc(
            "map2 = "
            "if(row() == 1 && col() == 1, 1, "
            "if(row() == 1 && col() >= 2, 2, "
            "if(row() == 2 && col() == 1, 2, "
            "if(row() == 2 && col() == 2, 1, "
            "if(row() == 2 && col() == 3, 3, "
            "if(row() >= 3, 3, null()))))))",
            overwrite=True,
            env=session.env,
        )
        yield session  # Pass the session to tests
