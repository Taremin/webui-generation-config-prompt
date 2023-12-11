import modules.scripts as scripts
import modules.extra_networks as extra_networks
import modules.processing as processing
import gradio as gr

class GenarationConfigPrompt(scripts.Script):  
    def title(self):
        return self.__class__.__name__
    
    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Accordion(self.title(), open=False):
            with gr.Row():
                with gr.Column(min_width=50, scale=1):
                    trigger = gr.Textbox(
                        label="Triger Word",
                        lines=1,
                        value="config",
                        interactive=True,
                        elem_id="genconfprompt_trigger_word"
                    )
                    
        return [trigger]
    
    def before_process_batch(self, p, trigger, *args, **kwargs):
        _, extra = extra_networks.parse_prompts([prompt + '' for prompt in p.prompts])
        configs = extra.get(trigger)
        
        if (configs is None):
            return

        for config in configs:
            if len(config.positional) == 0:
                continue
            
            class ConfigProcessor:
                def swap():
                    p.width, p.height = p.height, p.width
                    if hasattr(p, "rng"):
                        shape = list(p.rng.shape)
                        shape[1] = p.height // processing.opt_f
                        shape[2] = p.width // processing.opt_f
                        p.rng.shape = tuple(shape)

                def set():
                    for key, val in config.named.items():
                        if not hasattr(p, key):
                            continue
                        
                        value_type = type(getattr(p, key))
                        if key == "cfg_scale":
                            value_type = float
                            
                        setattr(p, key, value_type(val))
                        
                        if key == "width":
                            if hasattr(p, "rng"):
                                shape = list(p.rng.shape)
                                shape[2] = p.width // processing.opt_f
                                p.rng.shape = tuple(shape)
                        elif key == "height":
                            if hasattr(p, "rng"):
                                shape = list(p.rng.shape)
                                shape[1] = p.height // processing.opt_f
                                p.rng.shape = tuple(shape)
                        
            funcname = config.positional[0]
            if not hasattr(ConfigProcessor, funcname):
                continue
            
            func = getattr(ConfigProcessor, funcname)
            if not callable(func):
                continue
            
            func()
