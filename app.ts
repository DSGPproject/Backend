import express, { Request, Response } from "express";
import bcrypt from "bcryptjs";
import { generateToken } from "./auth";

const app = express();
const port = 3000;

app.use(express.json());

app.get("/", (req: Request, res: Response) => {
  res.send("Hello, Welcome to GreenGuard!");
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

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
