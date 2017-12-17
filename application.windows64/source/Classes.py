class Force():
    def __init__(self, x, y, r, f=[0, 0]):
        self.x = x
        self.y = y
        self.r = r
        self.f = f

    def applyForce(self, particles):
        for p in particles:
            dx = self.x - p.s[0]
            dy = self.y - p.s[1]
            if sqrt(dx ** 2 + dy ** 2) < self.r:
                p.addForce(self.f)
        fill(170, 170, 170)
        noStroke()
        ellipse(self.x, self.y, self.r*2, self.r*2)
        strokeWeight(25)
        stroke(0)
        line(self.x, self.y, self.x + self.f[0] * 50, self.y + self.f[1] * 50)

    def pointForce(self, particles, magnitude):
        for p in particles:
            dx = self.x - p.s[0]
            dy = self.y - p.s[1]
            vectMag = sqrt(dx ** 2 + dy ** 2)

            if vectMag < self.r:
                try:
                    tempx = dx / vectMag
                except:
                    tempx = 0
                try:
                    tempy = dy / vectMag
                except:
                    tempy = 0
                p.addForce([tempx * magnitude, tempy * magnitude])
        fill(255, 150 + magnitude * 100,  150 +magnitude*100)
        noStroke()
        ellipse(self.x, self.y, self.r*2, self.r*2)


class Particle():

    def __init__(self, x, y, m, bType, c):
        self.s = [x, y]
        self.v = [0, 0]
        self.a = [0, 0]
        self.m = m
        self.forces = []
        self.bType = bType
        self.c = c

    def step(self):

        f = [0, 0]
        for force in self.forces:
            f[0] += force[0]
            f[1] += force[1]
        self.forces = []

        self.a[0], self.a[1] = f[0] / self.m, f[1] / self.m
        self.v[0], self.v[1] = self.v[0] + self.a[0], self.v[1] + self.a[1]
        self.s[0], self.s[1] = self.s[0] + self.v[0], self.s[1] + self.v[1]

        if self.bType == True:
            if not -width / 2 <= self.s[0] <= width / 2:
                self.s[0] = -self.s[0]
            elif not -height / 2 <= self.s[1] <= height / 2:
                self.s[1] = -self.s[1]
        else:
            if not -width / 2 <= self.s[0] <= width / 2:
                self.v[0] = -self.v[0]
            elif not -height / 2 <= self.s[1] <= height / 2:
                self.v[1] = -self.v[1]

            #if self.s[0] > width/2: self.s[0] = width/2
            # elif self.s[0] < -width/2: self.s[0] = -width/2
            #if self.s[1] > height/2: self.s[1] = height/2
            # elif self.s[1] < -height/2: self.s[1] = -height/2
        
        if self.c == "p":
            stroke(255, 0, 0)
        elif self.c == "n":
            stroke(0, 0, 255)
        else:
            stroke(self.c, self.c, 125 *self.m, 180)
        
        strokeWeight(25)
        point(self.s[0], self.s[1])

    def hit(self, otherU, otherM, c):
        self.v[0] = (otherM * -otherU[0] - self.m * (c *
                                                     self.v[0] + self.v[0] + otherU[0]) / c) / (otherM - self.m)
        self.v[1] = (otherM * -otherU[1] - self.m * (c *
                                                     self.v[1] + self.v[1] + otherU[1]) / c) / (otherM - self.m)

    def gravField(self, particles, magnitude, fieldSize):
        for p in particles:
            dx = self.s[0] - p.s[0]
            dy = self.s[1] - p.s[1]
            vectMag = sqrt(dx ** 2 + dy ** 2)
            if vectMag < fieldSize:
                try:
                    tempx = dx / vectMag
                except:
                    tempx = 0
                try:
                    tempy = dy / vectMag
                except:
                    tempy = 0
                p.addForce([tempx * magnitude, tempy * magnitude])

    def addForce(self, f):
        self.forces.append(f)

    def fluidResist(self, viscosity):
        self.addForce([-self.v[0] * viscosity, -self.v[1] * viscosity])

    def getCoords(self):
        return [self.s[0], self.s[1]]