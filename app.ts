import express, { Request, Response } from "express";
import multer from "multer";
import { exec } from "child_process";
import bcrypt from "bcryptjs";
import { authenticateToken, generateToken } from "./auth";

const app = express();
const port = 3000;

// Configure multer for file uploads
const upload = multer({ dest: "uploads/" });
app.use(express.json({ limit: "50mb" }));

app.get("/", (req: Request, res: Response) => {
  res.send("Hello, Express with TypeScript!");
});

// Single route for file upload and model processing
app.post("/upload", (req, res) => {
  const { image } = req.body;
  if (image) {
    // Execute the first model (converted from Jupyter Notebook)
    exec(
      `python3 ESAoject_detection.py "${image}"`,
      (error, stdout, stderr) => {
        if (error) {
          console.error(`exec error: ${error}`);
          return res
            .status(500)
            .json({ message: "Internal server error when executing Model 1." });
        }
        if (!req.file) {
          return res.status(400).json({ message: "Please upload a file." });
        }
        // Check stdout to determine if it's a plant leaf
        if (
          stdout.includes("The image does not contain a plant leaf.") ||
          stdout.includes("Image does not contain a leaf.")
        ) {
          return res.status(400).json({ message: 0 });
        } else {
          // If a plant leaf, execute Model 2 to detect the disease
          exec(
            `python3 model_usage_script.py "${__dirname}/model2" "${req.file.path}"`,
            (error, stdout, stderr) => {
              if (error) {
                console.error(`exec error: ${error}`);
                return res.status(500).json({
                  message: "Internal server error when executing Model 2.",
                });
              }

              // Send the disease detection result back to the client
              res.json({ disease: stdout.trim() });
            }
          );
        }
      }
    );
  } else {
    res.status(400).json({ message: "Please upload a file." });
  }
});

// Login
app.post("/login", async (req, res) => {
  // Authenticate User
  // const user = users.find(user => user.username === req.body.username);
  const username = "testuser";
  const password = "test@123";

  if (username !== req.body.username) {
    res.status(400).json({ message: "Incorrect username" });
  }
  try {
    if (await bcrypt.compare(req.body.password, password)) {
      console.log("This is running");

      // Generate and send token
      const token = generateToken(username);
      res.json({ token });
    } else {
      res.status(400).json({ message: "Incorrect credentials" });
    }
  } catch {
    res.status(500).send();
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
