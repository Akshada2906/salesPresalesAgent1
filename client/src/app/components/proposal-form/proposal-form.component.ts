import { Component, inject } from "@angular/core";
import {
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from "@angular/forms";
import { HttpClient, HttpClientModule } from "@angular/common/http";
import { HttpErrorResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { CommonModule } from "@angular/common";
import { MatIconModule } from "@angular/material/icon";
import { MatProgressBarModule } from "@angular/material/progress-bar";
import { MarkdownModule } from "ngx-markdown";
import { HttpRequestsConstants } from "../../services/http-requests-constants";
import { catchError } from 'rxjs/operators';
import { of } from 'rxjs';
import { MarkdownToHtmlModule } from "../../markdown-to-html.module";

interface ProposalData {
  customer: string;
  title: string;
  requirements: string;
  completion: string;
  amount: number ;
}

interface ProposalSection {
  title: string;
  content: string;
  layout_rank: number;
}

interface GeneratedProposal {
  proposal: {
    [key: string]: ProposalSection;
  };
}

interface ProgressState {
  percentage: number;
  message: string;
}

@Component({
  selector: "app-proposal-form",
  templateUrl: "./proposal-form.component.html",
  styleUrls: ["./proposal-form.component.css"],
  standalone: true,
  imports: [
    FormsModule,
    CommonModule,
    ReactiveFormsModule,
    HttpClientModule,
    MatIconModule,
    MatProgressBarModule,
    MarkdownModule,
    MarkdownToHtmlModule
],
  providers: [HttpClient],
})
export class ProposalFormComponent {
  proposalForm: FormGroup;
  isLoading = false;
  proposal: ProposalSection[] = [];
  isEditing = false;
  progress: ProgressState = {
    percentage: 0,
    message: "",
  };

  private http = inject(HttpClient);
  private fb = inject(FormBuilder);

  private progressStates: ProgressState[] = [
    { percentage: 25, message: "Analyzing requirements and project scope..." },
    { percentage: 50, message: "Generating proposal structure and outline..." },
    {
      percentage: 75,
      message: "Searching relevant case studies from database...",
    },
    {
      percentage: 90,
      message: "Formatting and organizing proposal sections...",
    },
    { percentage: 100, message: "Finalizing your proposal..." },
  ];

  constructor() {
    this.proposalForm = this.fb.group({
      customer: ["", Validators.required],
      title: ["", Validators.required],
      requirements: ["", Validators.required],
      completion: [""],
      amount: [""],
    });
  }

  generateProposal(data: ProposalData): Observable<GeneratedProposal> {
    return this.http.post<GeneratedProposal>(
      HttpRequestsConstants.GENERATE_PROPOSAL,
      data
    );
  }

  private simulateProgress(): void {
    let currentIndex = 0;

    const progressInterval = setInterval(() => {
      if (currentIndex < this.progressStates.length) {
        this.progress = this.progressStates[currentIndex];
        currentIndex++;
      } else {
        clearInterval(progressInterval);
      }
    }, 3000);
  }

  handleSubmit(): void {
    if (this.proposalForm.invalid) {
      return;
    }
    const formData = this.proposalForm.value;
    const cleanedData = {
      customer: formData.customer.trim(),
      title: formData.title.trim(),
      requirements: formData.requirements.trim(),
      completion: formData.completion?.trim() || null,
      amount: formData.amount ? parseFloat(formData.amount) : 50000  
    };
 
    this.isLoading = true;
    this.progress = {
      percentage: 0,
      message: "Initiating proposal generation...",
    };
    this.simulateProgress();
 
    const maxRetries = 3;
    let retryCount = 0;
 
    const attemptGeneration = () => {
      this.generateProposal(cleanedData).subscribe({
        next: (result) => {
          const proposalSections = Object.values(result.proposal);
          proposalSections.sort((a, b) => a.layout_rank - b.layout_rank);
          this.proposal = proposalSections;
          this.isLoading = false;
          this.progress = { percentage: 0, message: "" };
        },
        error: (error: HttpErrorResponse) => {
          console.error("Error generating proposal:", error);
          if (error.status === 503 && retryCount < maxRetries) {
            retryCount++;
            this.progress = {
              percentage: this.progress.percentage,
              message: `Service busy, retrying (${retryCount}/${maxRetries})...`,
            };
            setTimeout(() => attemptGeneration(), 2000 * Math.pow(2, retryCount));
            return;
          }
 
          this.isLoading = false;
          this.progress = { percentage: 0, message: "" };
          let errorMessage = "An error occurred while generating the proposal.";
          if (error.status === 503) {
            errorMessage = "Service is temporarily unavailable. Please try again later.";
          }
          alert(errorMessage);
        },
      });
    };
 
    attemptGeneration();
  }

  toggleEdit(): void {
    this.isEditing = !this.isEditing;
  }

  downloadProposal(): void {
    const title = this.proposalForm.get('title')?.value || 'untitled';
  
    // Prepare the request payload
    const payload = {
      sections: this.proposal.map((section, index) => ({
        title: section.title,
        content: section.content,
        layout_rank: index
      })),
      title: title
    };

    // Make the HTTP request with response type 'blob'
    this.http.post(HttpRequestsConstants.SAVE_PROPOSAL, payload, {
      responseType: 'blob'
    })
      .pipe(
        catchError(error => {
          console.error('Error saving and downloading proposal:', error);
          alert('Failed to save and download proposal. Please try again.');
          return of(null);
        })
      )
      .subscribe(response => {
        if (response) {
          // Create and trigger download
          const blob = new Blob([response], {
            type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
          });
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `${title}_proposal.docx`;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          URL.revokeObjectURL(url);
        }
      });
  }

  get formControls() {
    return this.proposalForm.controls;
  }

  getErrorMessage(controlName: string): string {
    const control = this.proposalForm.get(controlName);
    if (control?.hasError("required")) {
      return `${
        controlName.charAt(0).toUpperCase() + controlName.slice(1)
      } is required`;
    }
    return "";
  }
}
