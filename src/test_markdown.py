import unittest
from markdown import *

class Test_MarkDown_Func(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_bad_input(self):
        with self.assertRaises(Exception):
            matches = extract_markdown_images([1, 2, 3])

    def test_extract_markdown_images_wrong_input(self):
        matches = extract_markdown_images("This is text with an [image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_no_input(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](http://Youtube.com)")
        self.assertListEqual([("link", "http://Youtube.com")], matches)

    def test_extract_markdown_links_bad_input(self):
        with self.assertRaises(Exception):
            matches = extract_markdown_links([1, 2, 3])

    def test_extract_markdown_links_no_input(self):
        matches = extract_markdown_links("")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_wrong_input(self):
        matches = extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([], matches)

    
if __name__ == "__main__":
    unittest.main()