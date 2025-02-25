import grass.script as gs
from grass.gunittest.case import TestCase
from grass.gunittest.main import test
from grass.gunittest.gmodules import SimpleModule

class TestRCross(TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up a temporary region and create test raster maps"""
        cls.use_temp_region()

        # Create custom_map with specific cell values based on row and column
        cls.runModule(
            "r.mapcalc",
            expression="custom_map = if(row() == 1 && col() == 1, 5, if(row() == 1 && col() == 2, 5.5, if(row() == 2 && col() == 2, 5, if(row() == 3 && col() >= 2, 5.5, null()))))",
            overwrite=True,
        )

        # Create custom_map1 with a grid of values from 1 to 9
        cls.runModule(
            "r.mapcalc",
            expression="custom_map1 = if(row() == 1 && col() == 1, 1, if(row() == 1 && col() == 2, 2, if(row() == 1 && col() == 3, 3, if(row() == 2 && col() == 1, 4, if(row() == 2 && col() == 2, 5, if(row() == 2 && col() == 3, 6, if(row() == 3 && col() == 1, 7, if(row() == 3 && col() == 2, 8, if(row() == 3 && col() == 3, 9, null())))))))))",
            overwrite=True,
        )

    @classmethod
    def tearDownClass(cls):
        """Remove temporary maps and region"""
        cls.runModule("g.remove", flags="f", type="raster", name=["custom_map", "custom_map1"])
        cls.del_temp_region()
    
    def results_check(self, actual_categories, expected_categories):
        # Test if keys match
        assert set(actual_categories.keys()) == set(expected_categories.keys())

        # Test to check if labels are empty
        for key in expected_categories.keys():
            assert actual_categories[key] == expected_categories[key]


    def test_clump_basic(self):
        """Test basic clumped map."""
        gs.run_command(
            "r.clump",
            input="custom_map",
            output="clumped_map",
            overwrite=True
        )

        output_maps = gs.parse_command("g.list", type="raster")
        assert "clumped_map" in output_maps, "Output raster map 'clumped_map' should exist"

        category_output = gs.parse_command("r.category", map="clumped_map", format="json")

        print (category_output)

        actual_categories = {
            int(line.split("\t")[0]): line.split("\t")[1].strip() if "\t" in line else ""
            for line in category_output
        }

        expected_categories = {1: "", 2: "", 3: "", 4: ""}

        self.results_check(actual_categories, expected_categories)


    def test_clump_diagonal(self):
        """Test clumped map with diagonal connectivity."""
        gs.run_command(
            "r.clump",
            input="custom_map",
            output="clumped_map",
            flags="d",
            overwrite=True
        )

        output_maps = gs.parse_command("g.list", type="raster")
        assert "clumped_map" in output_maps, "Output raster map 'clumped_map' should exist"

        category_output = gs.parse_command("r.category", map="clumped_map")

        actual_categories = {
            int(line.split("\t")[0]): line.split("\t")[1].strip() if "\t" in line else ""
            for line in category_output
        }

        expected_categories = {1: "", 2: "", 3: ""}

        self.results_check(actual_categories, expected_categories)


    def test_clump_minsize(self):
        """Test clumped map with minimum size parameter."""
        gs.run_command(
            "r.clump",
            input="custom_map",
            output="clumped_map",
            minsize=2,
            overwrite=True
        )

        output_maps = gs.parse_command("g.list", type="raster")
        assert "clumped_map" in output_maps, "Output raster map 'clumped_map' should exist"

        category_output = gs.parse_command("r.category", map="clumped_map")

        actual_categories = {
            int(line.split("\t")[0]): line.split("\t")[1].strip() if "\t" in line else ""
            for line in category_output
        }

        expected_categories = {1: "", 2: ""}

        self.results_check(actual_categories, expected_categories)


    def test_clump_threshold(self):
        """Test clumped map with threshold parameter."""
        gs.run_command(
            "r.clump",
            input="custom_map1",
            output="clumped_map",
            threshold=0.2,
            overwrite=True
        )

        output_maps = gs.parse_command("g.list", type="raster")
        assert "clumped_map" in output_maps, "Output raster map 'clumped_map' should exist"

        category_output = gs.parse_command("r.category", map="clumped_map")

        actual_categories = {
            int(line.split("\t")[0]): line.split("\t")[1].strip() if "\t" in line else ""
            for line in category_output
        }

        expected_categories = {1: "", 2: "", 3: ""}

        self.results_check(actual_categories, expected_categories)

if __name__ == "__main__":
    test()
