import Classes

def mouseReleased():
    if mouseButton == RIGHT:
        if key not in ("1", "2"):
            dx = (mouseX - pmouseX) / 10.0
            dy = (mouseY - pmouseY) / 10.0
            if dy == 0 and dx == 0:
                forces.append(
                    Classes.Force(mouseX - width / 2, mouseY - height / 2, 50, [dx * 0.5, dy * 0.5]))
            else:
                pointForces.append(
                    Classes.Force(mouseX - width / 2, mouseY - height / 2, 50))

def setup():
    size(800, 800)
    global mode
    mode = 1
    global g
    g = 0.1
    global mass
    mass = 1
    modeInit(mode)

def draw():
    translate(width / 2, height / 2)
    background(200)

    if keyPressed:
        if key == "r":
            modeInit(mode)
        if key == "g":
            global gravity
            gravity = not gravity
        if key == "h":
            global g
            g += 0.01
        if key == "y":
            global g
            g -= 0.01    
        

    if mousePressed:
        if mouseButton == LEFT:
            global mode
            if 10 < mouseX < 40 and 10 < mouseY < 40:
                if mode == 1:
                    mode = 2
                elif mode == 2:
                    mode = 1
                modeInit(mode)
            elif 40 < mouseX < 70 and 10 < mouseY < 40:
                global mass
                mass += 1
                if mass == 3:
                    mass = 1
            
            else:
                for i in range(1):
                    dx = (mouseX - pmouseX) / 10.0
                    dy = (mouseY - pmouseY) / 10.0
                    
                    if mode == 1:
                        particles.append(
                            Classes.Particle(mouseX - width / 2, mouseY - height / 2, mass, True, 0))
                        particles[-
                                1].addForce([dx + random(-1, 1), dy + random(-0.2, 0.2)])
                        
                    elif mode == 2:
                        if key == "p":
                            posParticles.append(
                                Classes.Particle(mouseX - width / 2, mouseY - height / 2, 1, True, "p"))
                            posParticles[-
                                        1].addForce([dx + random(-1, 1), dy + random(-1, 1)])
                        if key == "o":
                            negParticles.append(
                                Classes.Particle(mouseX - width / 2, mouseY - height / 2, 1, True, "n"))
                            negParticles[-
                                        1].addForce([dx + random(-1, 1), dy + random(-1, 1)])
            
    if gravity == True:
        for p in particles:
            p.addForce([0, g])
    if mode == 1:
        for f in pointForces:
            f.pointForce(particles, 0.1)
        for f in forces:
            f.pointForce(particles, -3)
            
        for p in particles:
            p.gravField(particles, -1, 5)
            p.gravField(particles, -0.1, 25)
            p.gravField(particles, 0.01, 50)
            p.fluidResist(0.1)
            p.step()
            
            
    elif mode == 2:
        for f in pointForces:
            f.pointForce(posParticles, 0.3)
            f.pointForce(negParticles, 0.3)
        for f in forces:
            f.applyForce(posParticles)
            f.applyForce(negParticles)
        for p in posParticles:
            p.gravField(posParticles, -0.02, 50)
            p.gravField(negParticles, 0.02, 50)
            p.fluidResist(0.01)
            p.step()
            
        for p in negParticles:
            p.gravField(posParticles, 0.02, 50)
            p.gravField(negParticles, -0.02, 50)
            p.fluidResist(0.01)
            p.step()
    noStroke()
    fill(mode * 70, 0, 0)
    rect(10 - width/2 ,10 - height/2, 30, 30)
    fill(0, mass * 70, 0)
    rect(40 - width/2 ,10 - height/2, 30, 30)
    

def modeInit(mode):
    global particles
    particles = []
    global forces
    forces = []
    global pointForces
    pointForces = []
    global gravity
    gravity = False

    if mode == 2:
        global posParticles
        posParticles = []
        global negParticles
        negParticles = []