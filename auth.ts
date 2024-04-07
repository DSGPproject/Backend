import jwt from "jsonwebtoken";
import { Request, Response, NextFunction } from "express";

const JWT_SECRET = "nZr4u7x!A%D*G-KaPdSgVkYp3s6v9y$B";

export function generateToken(userId: string) {
  return jwt.sign({ userId }, JWT_SECRET, { expiresIn: "1h" });
}

function verifyToken(token: string) {
  return jwt.verify(token, JWT_SECRET);
}

export function authenticateToken(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers["authorization"];
  const token = authHeader && authHeader.split(" ")[1]; // Bearer TOKEN
  if (token == null) return res.sendStatus(401);

  jwt.verify(token, JWT_SECRET, (err: any, user: any) => {
    if (err) return res.sendStatus(403);
    //   req.user = user;
    next();
  });
}
