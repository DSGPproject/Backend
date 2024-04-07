import express, { Request, Response } from "express";
import bcrypt from "bcryptjs";
import multer from "multer";
import { exec } from "child_process";
import { generateToken } from "./auth";

const app = express();
const port = 3000;

// Configure multer for file uploads
const upload = multer({ dest: "uploads/" });

app.use(express.json());

app.get("/", (req: Request, res: Response) => {
  res.send("Hello, Welcome to GreenGuard!");
});

// Single route for file upload and model processing
app.post("/upload", upload.single("photo"), (req, res) => {
  if (req.file) {
    // Execute the first model (converted from Jupyter Notebook)
    exec(
      `python3 ESAoject_detection.py "${req.file.path}"`,
      (error, stdout, stderr) => {
        if (error) {
          console.log(error);
          console.error(`exec error: ${error}`);
          return res
            .status(500)
            .json({ message: "Internal server error when executing Model 1." });
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
  const username = "testuser";
  const password = "test@123";

  if (username != req.body.password) {
    res.status(400).json({ message: "Incorrect username" });
  }

  try {
    if (await bcrypt.compare(req.body.password, password)) {
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
