import { CommonModule } from "@angular/common";
import { Component, Input } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { MatIconModule } from "@angular/material/icon";

@Component({
  selector: "app-chat-message",
  standalone: true,
  imports: [FormsModule, CommonModule, MatIconModule],
  templateUrl: "./chat-message.component.html",
  styleUrls: ["./chat-message.component.css"],
})
export class ChatMessageComponent {
  @Input() message: string = "";
  @Input() isBot: boolean = false;
  @Input() timestamp: string = "";
}
