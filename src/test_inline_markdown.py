import unittest
from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimeter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
    )

class TestSplitNodesDelimeter(unittest.TestCase):
    def test_basic_code_split(self):
        node = TextNode("This is `code` text", TextType.PLAIN_TEXT)
        result = split_nodes_delimeter([node], "`", TextType.CODE_TEXT)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.PLAIN_TEXT)

        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE_TEXT)
        
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.PLAIN_TEXT)

    def test_multiple_splits(self):
        node = TextNode("`a` b `c`", TextType.PLAIN_TEXT)
        result = split_nodes_delimeter([node], "`", TextType.CODE_TEXT)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text_type, TextType.CODE_TEXT)
        self.assertEqual(result[1].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(result[2].text_type, TextType.CODE_TEXT)

    def test_no_delimiter(self):
        node = TextNode("plain text", TextType.PLAIN_TEXT)
        result = split_nodes_delimeter([node], "`", TextType.CODE_TEXT)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "plain text")

    def test_unmatched_delimiter_raises(self):
        node = TextNode("this is `broken", TextType.PLAIN_TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimeter([node], "`", TextType.CODE_TEXT)

    def test_non_text_node_unchanged(self):
        node = TextNode("already bold", TextType.BOLD_TEXT)
        result = split_nodes_delimeter([node], "`", TextType.CODE_TEXT)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], node)

class TestMarkdownExtraction(unittest.TestCase):

    # ----- IMAGE TESTS -----

    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches
        )

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![one](url1) and ![two](url2)"
        )
        self.assertListEqual(
            [("one", "url1"), ("two", "url2")],
            matches
        )

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("no images here")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty_alt(self):
        matches = extract_markdown_images("![](url)")
        self.assertListEqual([("", "url")], matches)

    def test_extract_markdown_images_ignores_links(self):
        matches = extract_markdown_images("[link](url)")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_mixed_content(self):
        matches = extract_markdown_images(
            "text ![img1](url1) more text ![img2](url2)"
        )
        self.assertListEqual(
            [("img1", "url1"), ("img2", "url2")],
            matches
        )

    # ----- LINK TESTS -----

    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links(
            "A link to [Google](https://google.com)"
        )
        self.assertListEqual(
            [("Google", "https://google.com")],
            matches
        )

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "[one](url1) and [two](url2)"
        )
        self.assertListEqual(
            [("one", "url1"), ("two", "url2")],
            matches
        )

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("no links here")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_ignores_images(self):
        matches = extract_markdown_links(
            "![img](url) and [link](url2)"
        )
        self.assertListEqual(
            [("link", "url2")],
            matches
        )

    def test_extract_markdown_links_empty_text(self):
        matches = extract_markdown_links("[](url)")
        self.assertListEqual([("", "url")], matches)

class TestSplitNodes(unittest.TestCase):

    # ----- IMAGE TESTS -----

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE_TEXT, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGE_TEXT, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("Just plain text here", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])

        self.assertListEqual([node], new_nodes)

    def test_split_images_back_to_back(self):
        node = TextNode(
            "![a](url1)![b](url2)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE_TEXT, "url1"),
                TextNode("b", TextType.IMAGE_TEXT, "url2"),
            ],
            new_nodes,
        )

    # ----- LINK TESTS -----

    def test_split_links(self):
        node = TextNode(
            "Click here [Google](https://google.com)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Click here ", TextType.PLAIN_TEXT),
                TextNode("Google", TextType.LINK_TEXT, "https://google.com"),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("Just text, no links", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])

        self.assertListEqual([node], new_nodes)

    def test_split_links_multiple(self):
        node = TextNode(
            "Visit [Google](https://google.com) and [YouTube](https://youtube.com)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Visit ", TextType.PLAIN_TEXT),
                TextNode("Google", TextType.LINK_TEXT, "https://google.com"),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode("YouTube", TextType.LINK_TEXT, "https://youtube.com"),
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("obi wan image", TextType.IMAGE_TEXT, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK_TEXT, "https://boot.dev"),
        ]   
        assert nodes == expected

    def test_text_to_textnodes_plain_text(self):
        text = "just text"
        assert text_to_textnodes(text) == [
            TextNode("just text", TextType.PLAIN_TEXT)
        ]

    def test_text_to_textnodes_multiple_formats(self):
        text = "**bold** and _italic_"
        nodes = text_to_textnodes(text)

        assert nodes == [
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
        ]

    def test_text_to_textnodes_adjacent(self):
        text = "**bold**_italic_"
        nodes = text_to_textnodes(text)

        assert nodes == [
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
        ]

if __name__ == "__main__":
    unittest.main()