import omni.replicator.core as rep

lie_happened = False
with rep.new_layer():
    def get_apples():
        apples = rep.get.prims(semantics=[("class", "apple")])
        with apples:
            rep.physics.collider()
            rep.modify.visibility(rep.distribution.choice([True, False]))
            rep.modify.pose(
                position=rep.distribution.normal((0.0, 5.0, 0.0), (35, 0.0, 35)),
                rotation=rep.distribution.uniform((-180,-180, -180), (180, 180, 180)),
                # scale=rep.distribution.normal(1, 0.5)
            )
        return apples.node
    
    def get_lemons():
        lemons = rep.get.prims(semantics=[("arbitrary", "lemon")])
        with lemons:
            rep.physics.collider()
            rep.modify.visibility(rep.distribution.choice([True, False]))
            rep.modify.pose(
                position=rep.distribution.normal((0.0, 5.0, 0.0), (20, 0.0, 20)),
                rotation=rep.distribution.uniform((-180,-180, -180), (180, 180, 180)),
                # scale=rep.distribution.normal(1, 0.5)
            )
        return lemons.node


    def get_bottles():
        bottles = rep.get.prims(semantics=[("arbitrary", "bottle")])
        with bottles:
            rep.physics.collider()
            rep.modify.visibility(rep.distribution.choice([True, False], weights=[0.2, 0.8]))              
            rep.modify.pose(
                position=rep.distribution.uniform((-100, 11.6, -100), (100, 11.6, 100)),
                rotation=rep.distribution.uniform((0, -180, 0), (0, 180, 0)),
                # scale=rep.distribution.normal(1, 0.5)
            )
        return bottles.node

    def get_oranges():
        oranges = rep.get.prims(semantics=[("arbitrary", "orange")])
        with oranges:
            rep.physics.collider()
            rep.modify.visibility(rep.distribution.choice([True, False]))              
            rep.modify.pose(
                position=rep.distribution.uniform((-100, 3.5, -100), (100, 3.5, 100)),
                rotation=rep.distribution.uniform((-180,-180, -180), (180, 180, 180)),
                # scale=rep.distribution.normal(1, 0.5)
            )
        return oranges.node

    def get_others():
        others = rep.get.prims(semantics=[("arbitrary", "others")])
        with others:
            rep.physics.collider()
            rep.modify.visibility(rep.distribution.choice([True, False]))              
            rep.modify.pose(
                position=rep.distribution.uniform((-100, 0, -100), (100, 0, 100)),
                rotation=rep.distribution.uniform((0, -180, 0), (0, 180, 0)),
                # scale=rep.distribution.normal(1, 0.5)
            )
        return others.node

    def sphere_lights():
        lights = rep.create.light(
            light_type="Sphere",
            temperature=rep.distribution.normal(4500, 2000),
            intensity=rep.distribution.normal(30000, 5000),
            position=rep.distribution.uniform((-150, 200, -150), (150, 300, 150)),
            scale=rep.distribution.uniform(50, 100),
            count=2
        )
        return lights.node
        
    def get_plane():
        plane = rep.get.prims("/World/Plane")
        with plane:
            rep.physics.collider()
            rep.randomizer.materials(materials=rep.distribution.choice([
            "omniverse://localhost/NVIDIA/Materials/Base/Wood/Walnut.mdl",
            "omniverse://localhost/NVIDIA/Materials/Base/Wood/Mahogany.mdl",
            "omniverse://localhost/NVIDIA/Materials/Base/Wall_Board/Cardboard.mdl",
            "omniverse://localhost/NVIDIA/Materials/Base/Natural/Grass_Cut.mdl"
            ]))
        return plane.node


    rep.randomizer.register(get_apples)
    rep.randomizer.register(get_lemons)
    rep.randomizer.register(sphere_lights)
    rep.randomizer.register(get_plane)
    rep.randomizer.register(get_bottles)
    rep.randomizer.register(get_oranges)
    rep.randomizer.register(get_others)

    camera = rep.create.camera()
    # Set the renderer to Path Traced
    #rep.settings.set_render_pathtraced(samples_per_pixel=1024)
    # Create the render product
    render_product  = rep.create.render_product(camera, (720, 720))
# Get a Kitti Writer and initialize its defaults
    writer = rep.WriterRegistry.get("KittiWriter")
    writer.initialize( output_dir=r"C:\Users\Vlad\Desktop\diploma_datasets\test_output\test_apples", bbox_height_threshold=5, fully_visible_threshold=0.75, omit_semantic_type=True)
    writer.attach([render_product])


    with rep.trigger.on_frame(num_frames=200, rt_subframes=200):
        rep.randomizer.sphere_lights()
        rep.randomizer.get_lemons()
        rep.randomizer.get_plane()
        rep.randomizer.get_apples()
        rep.randomizer.get_bottles()
        rep.randomizer.get_oranges()
        rep.randomizer.get_others()

        with camera:
            rep.modify.pose(position=rep.distribution.uniform((-75, 0, -75), (75, 50, 75)), look_at=(0,0,0))

