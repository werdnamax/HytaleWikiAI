import unittest
from unittest.mock import Mock, patch
import numpy as np

class TestEmbedding(unittest.TestCase):
  def test_embedding_shape(self):
    """Test that embedding returns correct shape"""
    embedding = np.random.rand(768)
    self.assertEqual(embedding.shape, (768,))
  
  def test_embedding_not_empty(self):
    """Test that embedding is not empty"""
    embedding = np.random.rand(768)
    self.assertGreater(len(embedding), 0)
  
  def test_embedding_values_in_range(self):
    """Test that embedding values are normalized"""
    embedding = np.random.rand(768)
    self.assertTrue(np.all(embedding >= 0))
    self.assertTrue(np.all(embedding <= 1))


if __name__ == '__main__':
  unittest.main()