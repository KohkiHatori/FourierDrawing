const api_url = "http://127.0.0.1:3000/image";

async function upload() {
  // This function is called when the upload button on html is pressed.
  // It uploads the input image to the backend API and receives the drawing data of the image. If there is no file selected, it gives an error.
  let formData = new FormData();
  if (fileupload.files.length > 0) {
    formData.append("file", fileupload.files[0]);
    try {
      await fetch(api_url, { method: "POST", body: formData })
        .then((response) => {
          return response.json().then((data) => {
            const drawing_data = JSON.parse(data);
            if (response.ok) {
              main(drawing_data);
            }
          })
        })
    } catch (err) {
      alert("Invalid File!");
    }

  } else {
    alert("Please choose an image file!");
  }
}

class Animation {

  // This class holds all the variables, constants and methods required to run the animation on html.

  constructor(lims, sets_of_coeffs) {
    this.sets_of_coeffs = sets_of_coeffs;
    this.init_constants_and_variables();
    this.factor = this.get_zoom_factor(lims);
    // this.factor is multiplies to the coordinates for the drawing to fit the screen
    this.init_canvas();
    this.init_control_panel();
    this.init_comp_vectors();
    this.sets_of_previous = Array(Object.keys(sets_of_coeffs).length);
    // This arrays stores the coordinates in the previous frame for each edge(set of coefficient), so that the path can be drawn.
    this.init_html();
    this.draw();
    // This is called to draw the first frame of the animation.
  }

  init_constants_and_variables() {
    // This method initializez the constans and variables

    this.width = window.innerWidth
    // width of the canvases
    this.height = window.innerHeight
    // height of the canvases
    this.origin = [0, this.height];
    // where the cartesian origin should be on the canvas coordinates
    this.DT = 0.001;
    // The time step
    this.margin_factor = 0.9;
    // How small the canvases should be on the screen. Margin factor of 1 will fill the whole screen
    this.pause_start = ["PAUSE", "START"];
    // The strings used for the toggle-aimation button
    this.path_colour = "cyan";
    this.vector_colour = "white";
    this.circle_colour = "white";


    this.interval = 10;
    // The interval between each frame
    this.num_vec = 200;
    // The number of vectors used for each edge
    // How much the original coordinates are multiplied by,  in order for the animation to fit the canvas
    this.show_circle = true;
    this.show_vector = true;
    this.pause = true;
    this.quit = false;
    this.t = 0;
  }

  get_zoom_factor(lims) {
    // This method computes the zoom factor
    let xlim = lims["x"];
    let ylim = lims["y"];
    let x_ratio = this.width / xlim[1];
    // The ratio between the screen width and the width of the image
    let y_ratio = this.height / ylim[1];
    // The ratio between the screen height and the height of the image
    let zoom_factor = Math.min(x_ratio, y_ratio) * this.margin_factor;
    // It takes the smallest of the two ratios and multiplies by the margin factor.
    return zoom_factor;
  }


  init_canvas() {
    // This method initilalizes the two canvases.
    this.anim = new Canvas(this.width, this.height, "anim");
    this.path = new Canvas(this.width, this.height, "path");
  }

  init_control_panel() {
    // This method initializes the control panel.
    this.control_panel = {
      quit_button: document.getElementById("quit-button"),
      clear_button: document.getElementById("clear-button"),
      toggle_animation_button: document.getElementById("toggle-animation"),
      toggle_circle_button: document.getElementById("toggle-circle"),
      toggle_vector_button: document.getElementById("toggle-vector"),
      num_vec_slider: document.getElementById("num-vec-slider"),
      num_vec_label: document.getElementById("num-vec"),
      speed_slider: document.getElementById("speed-slider"),
      speed_label: document.getElementById("speed")
    }
    this.init_num_vec_slider();
    this.add_event_listeners();
  }

  init_num_vec_slider() {
    // This method initializes the num_vec_slider
    this.control_panel.num_vec_slider.max = this.num_vec;
    // Sets the maximum value of the slider to this.num_vec
    this.control_panel.num_vec_slider.value = this.num_vec;
    // Sets the  value of the slider to this.num_vec
    this.control_panel.num_vec_label.innerText = this.num_vec;
    // Sets the  string of the slider label to this.num_vec
  }

  add_event_listeners() {
    // This method adds EventListeners to each button, stating which function is to be called when they are pressed
    this.control_panel.quit_button.addEventListener("click", (e) => { this.exit(); });
    this.control_panel.clear_button.addEventListener("click", (e) => { this.erase_path(); });
    this.control_panel.toggle_animation_button.addEventListener("click", (e) => { this.toggle_animation(); });
    this.control_panel.toggle_circle_button.addEventListener("change", (e) => { this.toggle_circle(); });
    this.control_panel.toggle_vector_button.addEventListener("change", (e) => { this.toggle_vector(); });
    this.control_panel.num_vec_slider.addEventListener("change", (e) => { this.change_num_vec(); });
    this.control_panel.speed_slider.addEventListener("change", (e) => { this.change_speed(); });
    document.body.onkeyup = (e) => { this.manage_keyups(e); }
    document.body.onkeydown = (e) => { this.manage_keydowns(e); }
  }

  manage_keyups(e) {
    // This method manages the keyup events
    if (e.key == " " || e.code == "Space" || e.keyCode == 32) {
      this.toggle_animation();
    } else if (e.key == "q" || e.code == "KeyQ" || e.keyCode == 81) {
      this.exit();
    } else if (e.key == "Backspace" || e.code == "Backspace" || e.keyCode == 8) {
      this.erase_path();
    }
  }

  manage_keydowns(e) {
    // This method manages the keydown events
    if (e.key == "ArrowLeft" || e.code == "ArrowLeft" || e.keyCode == 37) {
      this.decrement_num_vec();
    } else if (e.key == "ArrowRight" || e.code == "ArrowRight" || e.keyCode == 39) {
      this.increment_num_vec();
    }
  }

  init_comp_vectors() {
    // This method initializes the ComplexVector objects for each coefficient
    this.sets_of_comp_vectors = [];
    for (let coeffs of this.sets_of_coeffs) {
      var n = 0;
      // n is the frequency. It should be in the order 0, 1, -1, 2, -2, 3, -3, ....
      let comp_vectors = [];
      for (let i = 0; i < this.num_vec; i++) {
        let comp_vector = new ComplexVector(coeffs[n], n);
        comp_vectors.push(comp_vector);
        if (i % 2 == 0) {
          n += i + 1;
          // When the index is even, the difference between the current n and the next n is i + 1.
        } else {
          n *= -1;
          // When the index is odd, the next n should be minus the current index.
        }
      }
      this.sets_of_comp_vectors.push(comp_vectors);
    }
  }

  init_html() {
    // This method initializes the html file for the animation to take place.
    document.getElementsByClassName("animation-wrapper")[0].style.display = "block";
    document.getElementsByClassName("image-post")[0].style.display = "none";
    this.control_panel.toggle_animation_button.innerText = this.pause_start[+this.pause];
  }

  exit() {
    // This method reloads the page to exit the animation.
    location.reload();
  }

  erase_path() {
    // This method clears the entire path canvas to erase the path
    this.path.ctx.clearRect(0, 0, this.width, this.height);
  }

  toggle_animation() {
    // This method toggles the value of this.pause, starts and pauses the animation according to the value of the this.pause
    this.pause = !this.pause;
    this.control_panel.toggle_animation_button.innerText = this.pause_start[+this.pause];
    // It changes the inner text of the buttont to the correct string in the this.pause_start array.
    if (!this.pause) {
      // If this.pause is false, it starts the animation
      this.animate();
    }
  }

  update_canvas() {
    // This method clears the entire canvas and draws the next frame to account for any change made to this.show_circle or this.show_vector
    this.anim.ctx.clearRect(0, 0, this.width, this.height);
    this.draw();
  }

  toggle_circle() {
    // This method toggles the value of this.show_circle and updates the canvas, when the toggle button on html is pressed
    this.show_circle = !this.show_circle;
    this.update_canvas();
  }

  toggle_vector() {
    // This method toggles the value of this.show_vector and updates the canvas, when the toggle button on html is pressed
    this.show_vector = !this.show_vector;
    this.update_canvas();
  }

  change_num_vec() {
    // This method changes the number of vectors used for each path, when the slider value
    this.num_vec = Number(this.control_panel.num_vec_slider.value);
    // The value of the slider is converted to a Number object, as it is a string
    this.control_panel.num_vec_label.innerText = this.num_vec;
    // The label is changed to the value held by this.num_vec
  }


  change_speed() {
    // This method changes the speed of the animation by changing the value of interval between frames, when the value of the slider changes
    let speed = this.control_panel.speed_slider.value;
    this.interval = 11 - speed;
    // The speed ranges from 1 to 11, and the interval ranges from 0 to 10
    // The maximum speed is when there is no interval between frames, and when the speed is 1, the interval is at its maximum, 10.
    if (speed != 11) {
      this.control_panel.speed_label.innerText = speed;
    } else {
      this.control_panel.speed_label.innerText = "max";
    }
  }

  decrement_num_vec() {
    // This method decrements the number of vectors. It's executed when the left arrow key is pressed.
    this.num_vec -= 1;
    this.control_panel.num_vec_slider.value = this.num_vec;
    // Changes the value of the slider on html.
    this.control_panel.num_vec_label.innerText = this.num_vec;
    // Changes the text of the label
  }

  increment_num_vec() {
    // This method increments the number of vectors. It's executed when the right arrow key is pressed.
    this.num_vec += 1;
    this.control_panel.num_vec_slider.value = this.num_vec;
    // Changes the value of the slider on html.
    this.control_panel.num_vec_label.innerText = this.num_vec;
    // Changes the text of the label
  }


  async animate() {
    while (!(this.pause | this.quit)) {
      this.anim.ctx.clearRect(0, 0, this.width, this.height);
      this.draw();
      await new Promise(r => setTimeout(r, this.interval));
      // this is equivalent of time.sleep() in Python. It waits for this.interval amount of time.
      this.t += this.DT;
    }
  }


  draw_vector(ctx, previous_real, previous_imag, current_real, current_imag, colour) {
    // This method draws a vector from the input previous coordinates to the input current coordinates.
    ctx.beginPath();
    ctx.strokeStyle = colour;
    ctx.moveTo(previous_real, previous_imag);
    ctx.lineTo(current_real, current_imag);
    ctx.stroke();
  }

  draw_circle(current_real, current_imag, mag) {
    // This method draws a circle of which centre is the current coordinates and the radius is the input mag parameter
    this.anim.ctx.beginPath();
    this.anim.ctx.strokeStyle = this.circle_colour;
    this.anim.ctx.arc(current_real, current_imag, mag, 0, Math.PI * 2);
    this.anim.ctx.moveTo(current_real, current_imag);
    // This brings the pen tip back to the centre. This is done to avoid an extra line being drawn
    this.anim.ctx.stroke();
  }

  draw_path(current_real, current_imag, index) {
    // This method draws a part of path. Path is defined by numerous straight lines.
    // Every frame, a vector from the previous sum of all vectors for each edge to the current sum of all vectors for each edge is drawn
    let previous = this.sets_of_previous[index];
    if (previous != undefined && previous.length == 2) {
      // If previous sum exists, a vector is drawn
      this.draw_vector(this.path.ctx, previous[0], previous[1], current_real, current_imag, this.path_colour)
    }
  }

  transform_y(y_coordinate) {
    // This method transform y coordinate in cartesian coordinate system to screen coordinate system
    return - y_coordinate + this.height;
  }

  draw() {
    // This method draws out a frame on canvases
    var index = 0;
    for (let comp_vectors of this.sets_of_comp_vectors) {
      // for each edge, it draws vectors, circles and path
      this.anim.ctx.moveTo(origin[0], origin[1]);
      let current_real = 0;
      let current_imag = 0;
      for (let comp_vector of comp_vectors.slice(0, this.num_vec)) {
        // for each vector in the edge, it draws a circle and a vector on the anim canvas
        let vector = comp_vector.func(this.t);
        let real = vector[0] * this.factor;
        let imag = vector[1] * this.factor;
        let mag = comp_vector.mag * this.factor;
        // the coordinates and magnitude are multiplied by this.factor to fit user's screen
        if (this.show_circle) {
          this.draw_circle(current_real, this.transform_y(current_imag), mag);
        }
        let previous_real = current_real;
        let previous_imag = current_imag;
        current_real += real;
        current_imag += imag;
        // This updates the current coordinates
        if (this.show_vector) {
          this.draw_vector(this.anim.ctx, previous_real, this.transform_y(previous_imag), current_real, this.transform_y(current_imag), this.vector_colour);
        }
      }
      this.draw_path(current_real, this.transform_y(current_imag), index);
      this.sets_of_previous[index] = [current_real, this.transform_y(current_imag)];
      // This updates the previous sum.
      index++;
    }
  }


}

class Canvas {

  // Canvas holds data of the canvas element on html

  constructor(width, height, id) {
    this.elem = document.getElementById(id);
    this.elem.width = width;
    this.elem.height = height;
    this.ctx = this.elem.getContext("2d");
  }
}


class ComplexVector {

  // ComplexVector is a vector that constitutes the approximated function.

  constructor(coefficient, n) {
    this.coeff_real = coefficient[0];
    // real part of the coefficient
    this.coeff_imag = coefficient[1];
    // imaginary part of the coefficient
    this.n = n;
    // frequency of the vector
    this.mag = this.abs(this.func(0));
    // magnitude of the vector. This is a constant for any value of t, so it uses 0.
  }

  func(t) {
    // This method calculates the point on the complex plane at the time whent t = t
    let e_real = Math.cos(2 * Math.PI * this.n * t);
    // This is the real part of the complex vector, excluding the coefficient.
    let e_imag = Math.sin(2 * Math.PI * this.n * t);
    // This is the imaginary part of the complex vector, excluding the coefficient.
    let vector_real = this.coeff_real * e_real - this.coeff_imag * e_imag;
    // This is the real part of the complex vector after expanding the brackets
    let vector_imag = this.coeff_imag * e_real + this.coeff_real * e_imag;
    // This is the imaginary part of the complex vector after expanding the brackets
    return [vector_real, vector_imag];
  }

  abs(vector) {
    // This method returns the magnitude of a given vector
    return Math.sqrt(vector[0] ** 2 + vector[1] ** 2);
  }

}

function main(drawing_data) {
  // This function is run once the drawing data from the backend API is fetched. It unpacks the drawing data and creates an Animation object using the data.
  const lims = drawing_data["lim"];
  sets_of_coeffs = drawing_data["sets_of_coeffs"];
  anim_instance = new Animation(lims, sets_of_coeffs);
}
