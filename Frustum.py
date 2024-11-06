import numpy as np


class Frustum:
    def __init__(self, camera):
        self.camera = camera
        self.planes = np.zeros((6, 4))  # 6 planes (near, far, left, right, top, bottom), 4 coefficients each (A,B,C,D)
        self.update_planes()

    def update_planes(self):
        # Get camera parameters
        aspect = self.camera.render.WIDTH / self.camera.render.HEIGHT
        near = self.camera.near_plane
        far = self.camera.far_plane
        fov_h = self.camera.h_fov
        fov_v = self.camera.v_fov

        # Calculate frustum corners
        tang = np.tan(fov_h * 0.5)
        nh = near * tang
        nw = nh * aspect
        fh = far * tang
        fw = fh * aspect

        # Get camera vectors
        pos = self.camera.position[:3]
        forward = self.camera.forward[:3]
        right = self.camera.right[:3]
        up = self.camera.up[:3]

        # Calculate frustum centers
        nc = pos + forward * near
        fc = pos + forward * far

        # Calculate the 8 corners of the frustum
        ntl = nc + up * nh - right * nw
        ntr = nc + up * nh + right * nw
        nbl = nc - up * nh - right * nw
        nbr = nc - up * nh + right * nw

        ftl = fc + up * fh - right * fw
        ftr = fc + up * fh + right * fw
        fbl = fc - up * fh - right * fw
        fbr = fc - up * fh + right * fw

        # Calculate the six planes
        self.planes[0] = self._get_plane(ntr, ntl, nbl) # Near plane
        self.planes[1] = self._get_plane(ftl, ftr, fbr) # Far plane
        self.planes[2] = self._get_plane(ntl, ftl, fbl) # Left plane
        self.planes[3] = self._get_plane(ftr, ntr, nbr) # Right plane
        self.planes[4] = self._get_plane(ntl, ntr, ftr) # Top plane
        self.planes[5] = self._get_plane(nbr, nbl, fbl) # Bottom plane

    def _get_plane(self, p1, p2, p3):
        """Calculate plane equation Ax + By + Cz + D = 0 from three points"""
        v1 = p2 - p1
        v2 = p3 - p1
        normal = np.cross(v1, v2)
        normal = normal / np.linalg.norm(normal)
        d = -np.dot(normal, p1)
        return np.array([normal[0], normal[1], normal[2], d])

    def is_point_visible(self, point):
        """Test if a point is inside the frustum"""
        for plane in self.planes:
            if np.dot(plane[:3], point) + plane[3] < 0:
                return False
        return True

    def is_sphere_visible(self, center, radius):
        """Test if a sphere is inside or intersects the frustum"""
        # Always render if the camera is inside the sphere
        camera_pos = self.camera.position[:3]
        if np.linalg.norm(center - camera_pos) <= radius:
            return True

        for plane in self.planes:
            distance = np.dot(plane[:3], center) + plane[3]
            if distance < -radius:
                return False
        return True

    def is_point_in_front_of_near_plane(self, point):
        """Check if a point is in front of the near plane"""
        near_plane = self.planes[0]  # Assuming near plane is the first plane
        return np.dot(near_plane[:3], point) + near_plane[3] >= 0