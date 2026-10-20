"""Numerical edge-case smoke tests supplement — never replace — mathematical proofs."""
import math
import unittest


class MathBoundarySpotChecks(unittest.TestCase):
    def test_log_linear_root_boundary(self):
        a=math.exp(-1)
        x=1/a
        self.assertAlmostEqual(math.log(x)-a*x,0,places=12)
        for c in (0.25,0.3):
            self.assertGreater(math.log(1/c)-1,0)
        for c in (0.5,1.0):
            self.assertLess(math.log(1/c)-1,0)

    def test_exponential_ratio_minimum_at_one(self):
        y=math.e
        self.assertAlmostEqual(math.exp(1),y,places=12)
        for x in (0.05,0.5,2.0,4.0):
            self.assertGreater(math.exp(x)/x,y)

    def test_cubic_tangent_root_factorizations(self):
        for x in (-4,-1,0,1,2,4):
            # x^3 - 3x - 2 = (x+1)^2 (x-2)
            self.assertEqual(x**3-3*x-2,(x+1)**2*(x-2))
            # x^3 - 3x + 2 = (x-1)^2 (x+2)
            self.assertEqual(x**3-3*x+2,(x-1)**2*(x+2))

    def test_piecewise_monotonicity_jump_edge(self):
        a,b=1.0,0.0
        points=(-3,-1,-0.1,0,0.1,1,3)
        values=[x**3 if x<0 else a*x+b for x in points]
        self.assertTrue(all(u<v for u,v in zip(values,values[1:])))
        # a=1,b<0 breaks cross-piece strict monotonicity
        self.assertGreater((-0.01)**3,-0.5)


if __name__=='__main__':unittest.main()
