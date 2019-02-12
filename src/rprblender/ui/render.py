import pyrpr

from . import RPR_Panel


class RPR_RENDER_PT_devices(RPR_Panel):
    bl_label = "Render Devices"
    bl_context = 'render'

    def draw(self, context):
        devices = context.scene.rpr.devices

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        if len(pyrpr.Context.gpu_devices) == 0:
            col = layout.column(align=True)
            row = col.row()
            row.enabled = False
            row.prop(devices, 'cpu_state')
            col.prop(devices, 'cpu_threads')

        else:
            col = layout.column(align=True)
            col.prop(devices, 'cpu_state')
            row = col.row()
            row.enabled = devices.cpu_state
            row.prop(devices, 'cpu_threads')

            layout.separator()
            col = layout.column(align=True)
            for i in range(len(devices.gpu_states)):
                col.prop(devices, 'gpu_states', index=i, text=pyrpr.Context.gpu_devices[i]['name'])


class RPR_RENDER_PT_viewport_devices(RPR_Panel):
    bl_label = "Separate Viewport & Preview Devices"
    bl_parent_id = 'RPR_RENDER_PT_devices'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return super().poll(context) and len(pyrpr.Context.gpu_devices) > 0

    def draw_header(self, context):
        self.layout.prop(context.scene.rpr, "separate_viewport_devices", text="")
        self.layout.active = context.scene.rpr.separate_viewport_devices

    def draw(self, context):
        devices = context.scene.rpr.viewport_devices

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        self.layout.enabled = context.scene.rpr.separate_viewport_devices

        if len(pyrpr.Context.gpu_devices) == 0:
            col = layout.column(align=True)
            row = col.row()
            row.enabled = False
            row.prop(devices, 'cpu_state')
            col.prop(devices, 'cpu_threads')

        else:
            col = layout.column(align=True)
            col.prop(devices, 'cpu_state')
            row = col.row()
            row.enabled = devices.cpu_state
            row.prop(devices, 'cpu_threads')

            layout.separator()
            col = layout.column(align=True)
            for i in range(len(devices.gpu_states)):
                col.prop(devices, 'gpu_states', index=i, text=pyrpr.Context.gpu_devices[i]['name'])


class RPR_RENDER_PT_limits(RPR_Panel):
    bl_label = "Render Limits"
    bl_context = 'render'

    def draw(self, context):
        self.layout.use_property_split = True
        self.layout.use_property_decorate = False

        limits = context.scene.rpr.limits

        col = self.layout.column()
        col.prop(limits, 'type')
        col1 = col.column(align=True)
        if limits.type == 'ITERATIONS':
            col1.prop(limits, 'iterations')
        else:
            col.prop(limits, 'seconds')
        col1.prop(limits, 'update_samples')


class RPR_RENDER_PT_viewport_limits(RPR_Panel):
    bl_label = "Viewport & Preview Render Limits"
    bl_parent_id = 'RPR_RENDER_PT_limits'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        self.layout.use_property_split = True
        self.layout.use_property_decorate = False

        limits = context.scene.rpr.viewport_limits

        col = self.layout.column()
        col.prop(limits, 'type')
        if limits.type == 'ITERATIONS':
            col.prop(limits, 'iterations')
        else:
            col.prop(limits, 'seconds')

        col.separator()
        col.prop(limits, 'thumbnail_iterations')


class RPR_RENDER_PT_quality(RPR_Panel):
    bl_label = "Render Quality"
    bl_context = 'render'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        # This is a parent Panel for (RPR_RENDER_PT_max_ray_depth, RPR_RENDER_PT_light_clamping)
        pass


class RPR_RENDER_PT_max_ray_depth(RPR_Panel):
    bl_label = "Max Ray Depth"
    bl_parent_id = 'RPR_RENDER_PT_quality'

    def draw(self, context):
        self.layout.use_property_split = True
        self.layout.use_property_decorate = False

        rpr_scene = context.scene.rpr

        self.layout.prop(rpr_scene, 'max_ray_depth', slider=True)

        col = self.layout.column(align=True)
        col.prop(rpr_scene, 'diffuse_depth', slider=True)
        col.prop(rpr_scene, 'glossy_depth', slider=True)
        col.prop(rpr_scene, 'refraction_depth', slider=True)
        col.prop(rpr_scene, 'glossy_refraction_depth', slider=True)
        col.prop(rpr_scene, 'shadow_depth', slider=True)

        self.layout.prop(rpr_scene, 'ray_cast_epsilon', slider=True)


class RPR_RENDER_PT_light_clamping(RPR_Panel):
    bl_label = "Clamping"
    bl_parent_id = 'RPR_RENDER_PT_quality'

    def draw_header(self, context):
        self.layout.prop(context.scene.rpr, 'use_clamp_radiance', text="")

    def draw(self, context):
        self.layout.use_property_split = True
        self.layout.use_property_decorate = False

        rpr_scene = context.scene.rpr

        col = self.layout.column()
        col.enabled = rpr_scene.use_clamp_radiance
        col.prop(rpr_scene, 'clamp_radiance')


class RPR_RENDER_PT_effects(RPR_Panel):
    bl_label = "Render Effects"
    bl_context = 'render'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        rpr_scene = context.scene.rpr
        col = layout.column()
        col.prop(rpr_scene, 'use_render_stamp')
        col.prop(rpr_scene, 'render_stamp', text="")


class RPR_RENDER_PT_motion_blur(RPR_Panel):
    bl_label = "Motion Blur"
    bl_context = 'render'
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.prop(context.scene.rpr, 'motion_blur', text="")

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False

        rpr_scene = context.scene.rpr

        col = layout.column()
        col.enabled = rpr_scene.motion_blur
        col.prop(context.scene.rpr, 'motion_blur_exposure_apply')
        col.prop(context.scene.rpr, 'motion_blur_exposure')

        col.separator()
        col.prop(context.scene.rpr, 'motion_blur_scale_apply')
        col.prop(context.scene.rpr, 'motion_blur_scale')


class RPR_RENDER_PT_help_about(RPR_Panel):
    bl_label = "Help/About"
    bl_context = 'render'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        layout.label(text="Help/About page")
